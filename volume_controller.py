"""
volume_controller.py  (Windows version, using pycaw)
------------------------------------------------------
Ready-to-use class that turns a raw thumb-to-index distance into
system volume control. You do NOT need to edit this file.

This version sets the EXACT system volume directly (via pycaw),
instead of simulating volume-up/volume-down key presses. That gives
a true 1:1 mapping between hand distance and volume -- no lag, no
"why did it barely change" problem.

Install requirements:
    pip install pycaw comtypes opencv-python numpy

Usage in your own script:

    from volume_controller import VolumeController

    controller = VolumeController()

    # ... inside your loop, once you've computed `dist` yourself ...
    frame = controller.update(dist, frame)
"""

import time
import cv2
import numpy as np
from pycaw.pycaw import AudioUtilities


class VolumeController:
    def __init__(self, min_dist=0.02, max_dist=0.25,
                 mute_threshold=0.025, mute_cooldown=1.0):
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.mute_threshold = mute_threshold
        self.mute_cooldown = mute_cooldown

        self.last_mute_time = 0
        self.is_muted = False
        # self.vol_percent = 0

        # --- nnnnConnect to the Windows system audio endpoint ---
        # Newer pycaw exposes the volume interface directly via
        # .EndpointVolume, instead of the older .Activate(...) pattern.
        device = AudioUtilities.GetSpeakers()
        self.volume = device.EndpointVolume

    def update(self, dist, frame):
        """
        Call this once per frame with the thumb-index distance you computed.
        Returns the frame with the volume bar / status drawn on it.
        """
        now = time.time()

        # --- Mute toggle on full pinch ---
        if dist < self.mute_threshold and (now - self.last_mute_time) > self.mute_cooldown:
            self.is_muted = not self.is_muted
            self.volume.SetMute(1 if self.is_muted else 0, None)
            
            self.last_mute_time = now

        # --- Map distance directly to volume 0.0-1.0 and SET it exactly ---
        vol_scalar = np.interp(dist, [self.min_dist, self.max_dist], [0.0, 1.0])
        vol_scalar = float(np.clip(vol_scalar, 0.0, 1.0))
        self.volume.SetMasterVolumeLevelScalar(vol_scalar, None)
        self.vol_percent = int(vol_scalar * 100)

        # --- Draw volume % and bar ---
        cv2.putText(frame, f'Volume: {self.vol_percent}%', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

        bar_top, bar_bottom = 100, 300
        bar_fill = int(np.interp(self.vol_percent, [1, 100], [bar_bottom, bar_top]))
        cv2.rectangle(frame, (50, bar_top), (85, bar_bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (50, bar_fill), (85, bar_bottom), (0, 255, 0), cv2.FILLED)

        if self.is_muted:
            cv2.putText(frame, 'MUTED', (50, 350),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        return frame , self.vol_percent

    
    
