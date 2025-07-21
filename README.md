# Tello Drone Control & Face‑Tracking System

An end‑to‑end Python toolkit for piloting a DJI Tello drone **manually via the keyboard** or **autonomously through real‑time face tracking**. The project is built on top of the \[Tello SDK] and \[djitellopy] wrapper and comes with utilities for image capture, flight‑path visualisation, and on‑board PID tuning.

---

## Features

* **Manual RC control** using `pygame` with smooth 25 cm / 36 ° per‑tick motion primitives.
* **Auto take‑off / landing** helpers.
* **Face‑tracking follow‑mode** powered by OpenCV Haar cascades + 1‑D PID controller.
* **First‑person video stream** overlay + single‑key still‑image snapshots (`P`).
* **Live 2‑D flight‑path plot** rendered with OpenCV for quick debugging.
* Battery‑level read‑out on connection.

---

## Repository Layout

| Path               | Purpose                                                                                                                       |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| `drone_init.py`    | Lightweight wrapper that connects to the drone, starts video, and exposes `_launch()`, `_takeoff()`, `_land()`.               |
| `control.py`       | **Main entry‑point for manual flight.** Reads keyboard, integrates velocity → position, plots course, and drives the RC loop. |
| `keyboard.py`      | Pygame window & key‑polling helper; also handles image snapshots.                                                             |
| `vector.py`        | Dead‑reckoning + Cartesian plotting utility (250 ms control interval).                                                        |
| `image_capture.py` | Grabs current FPV frame, scales and displays or saves to `Drone/images/`.                                                     |
| `face_tracking.py` | Stand‑alone demo launching face‑tracking auto‑follow mode with PID parameters in `pid[]`.                                     |

---

## Requirements

* **Hardware**

  * DJI Tello (or Ryze Tello EDU)
  * 2.4 GHz Wi‑Fi adapter
* **Software**

  * Python ≥ 3.8
  * [`djitellopy` ≥ 2.4](https://github.com/damiafuentes/DJITelloPy)
  * `opencv‑python`
  * `pygame`
  * `numpy`

Install dependencies:

```bash
pip install djitellopy opencv-python pygame numpy
```

---

## Quick Start

1. Power on the drone and connect your PC to the **TELLO‑XXXXXX** Wi‑Fi network.
2. Open a terminal in the repo root.
3. **Manual flight:**

   ```bash
   python control.py
   ```

   **Face‑tracking demo:**

   ```bash
   python face_tracking.py
   ```

---

## Keyboard Controls (Manual Mode)

| Key       | Action              | Remarks                           |
| --------- | ------------------- | --------------------------------- |
| **T**     | Take‑off            | Starts video stream automatically |
| **ESC**   | Land + exit         | Always available                  |
| **W / S** | Forward / Backward  | 25 cm every 250 ms tick           |
| **A / D** | Strafe Left / Right | 25 cm every tick                  |
| **Z / X** | Up / Down           | 25 cm every tick                  |
| **Q / E** | Rotate CCW / CW     | 36 ° every tick                   |
| **P**     | Snapshot            | Saves JPEG under `Drone/images/`  |

> The small control granularity makes indoor testing safer. Adjust `vector.speed_x`, `vector.ang_v`, and `vector.itv` to tune step size.

---

## Face‑Tracking Mode

Running `face_tracking.py` will:

1. Automatically **take off** and ascend 25 cm.
2. Continuously search for the **largest face** in the frame using OpenCV’s Haar cascade.
3. Apply a PID controller (`pid = [Kp, Kd, Ki]`) to align the face horizontally and regulate distance (via forward/backward commands).
4. **Land** safely when you press **Q** in the video window.

You can tweak:

```python
fbr = [6200, 6800]  # acceptable face‑bounding‑box area range
pid = [0.4, 0.4, 0] # PID gains (P, D, I)
```

---

## Flight‑Path Plotting

During manual control, a separate OpenCV window shows a **top‑down 2‑D trace** of the drone’s motion (red dot). This provides quick feedback when GPS is unavailable.

* Cartesian coordinates are accumulated in `vector.get_cartesian()`.
* Call frequency and scale can be tuned via `vector.itv` and `vector.ditv`.

---

## Development Notes

* **Motion primitives** are mapped through `control.transformation()` returning a 4‑element RC vector `[left/right, fwd/back, up/down, yaw]`.
* The `keyboard` module decouples input so you can later swap in gamepad or ROS topics.
* All blocking delays are minimal (`time.sleep(0.05)`) to keep the loop ≈20 Hz.

---

## Safety & Disclaimer

* Test in a **spacious indoor area** with prop guards.
* Maintain visual line‑of‑sight at all times.
* This code is provided **as‑is** without warranty; fly responsibly and comply with your local UAV regulations.

---

## Licence

MIT © 2025 Enze Zhang

