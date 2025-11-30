from manim import *
import numpy as np

class DiffusionPulse(ThreeDScene):
    def construct(self):
        # 1. Camera Setup
        self.camera.background_color = BLACK
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES, zoom=0.8)

        # 2. Time Control
        # We simulate time 't' moving from a small value (sharp peak) to a large value (flat ripple)
        # We use a ValueTracker so the surface can update dynamically.
        t_tracker = ValueTracker(0.2)

        # 3. Dynamic Surface Definition
        # We use always_redraw to recalculate the surface mesh every frame based on t_tracker
        def get_surface():
            t = t_tracker.get_value()

            # Constants to tune the visual physics
            frequency = 4.0      # How close the ripple rings are
            wave_speed = 3.0     # How fast ripples move out
            decay_rate = 1.0     # How fast the height collapses
            spread_rate = 2.0    # How fast the width expands

            # The Function
            # z = (Amplitude) * (Wave) * (Gaussian Envelope)
            func = lambda u, v: np.array([
                u,
                v,
                (1.5 / (t ** decay_rate)) *                     # Amplitude drops as 1/t
                np.cos(frequency * np.sqrt(u**2 + v**2) - wave_speed * t) *  # Traveling Wave
                np.exp(-(u**2 + v**2) / (spread_rate * t))      # Gaussian spreading width
            ])

            return Surface(
                func,
                u_range=[-5, 5],
                v_range=[-5, 5],
                resolution=(48, 48), # High resolution to catch the sharp initial spike
            ).set_style(
                fill_opacity=0,
                stroke_color=WHITE,
                stroke_width=1.5
            )

        # 4. Initialize and Animate
        surface = always_redraw(get_surface)
        self.add(surface)

        # Optional: Add axis for scale reference (faded)
        # axes = ThreeDAxes().set_opacity(0.3)
        # self.add(axes)

        # ANIMATION SEQUENCE

        # Phase 1: The Diffusion
        # We animate the time tracker from 0.2 (sharp spike) to 4.0 (spread out wave)
        self.play(
            t_tracker.animate.set_value(4.0),
            run_time=6,
            rate_func=linear # Linear makes the physics look more natural
        )

        # Phase 2: Rotation to admire the final state
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(2)


# To render:
# manim -pql src/diffusion_scene.py DiffusionPulse
# manim -pqh src/diffusion_scene.py DiffusionPulse  (high quality)
