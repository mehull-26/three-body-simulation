import yaml
import math
import numpy as np
import matplotlib.pyplot as plt

plt.ion()

fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

scat = ax.scatter([], [])


class body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)

    def apply_force(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt

    def update_position(self, dt):
        self.position += self.velocity * dt


def load_config(path):
    """Loads configuration settings from YAML files"""
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


def initialize_bodies(config):
    bodies = []
    for b in config["bodies"]:
        bodies.append(body(b["mass"], b["position"], b["velocity"]))

    return bodies


def resolve_forces(bodies, G):
    f_m1_m2 = calculate_force(bodies[0], bodies[1], G)
    f_m2_m3 = calculate_force(bodies[1], bodies[2], G)
    f_m1_m3 = calculate_force(bodies[0], bodies[2], G)
    forces = [f_m1_m2 + f_m1_m3, f_m2_m3 - f_m1_m2, -1 * f_m2_m3 - f_m1_m3]

    return forces


def calculate_force(b1, b2, G):
    """Force on b1 due to b2"""
    m1 = b1.mass
    m2 = b2.mass
    pos1 = b1.position
    pos2 = b2.position

    eps = 1e-3
    r = np.linalg.norm(pos1 - pos2) + eps

    return (pos2 - pos1) * G * m1 * m2 / r**3


def run_simulation(bodies, config):
    dt = config["simulation"]["dt"]
    steps = config["simulation"]["steps"]
    G = config["simulation"]["G"]

    for j in range(0, steps):
        forces = resolve_forces(bodies, G)
        for i in range(0, 3):
            bodies[i].apply_force(forces[i], dt)
            bodies[i].update_position(dt)

        positions = [body.position for body in bodies]
        x = [p[0] for p in positions]
        y = [p[1] for p in positions]

        scat.set_offsets(list(zip(x, y)))
        ax.relim()
        ax.autoscale_view()
        plt.pause(0.01)

    return


def main():

    config = load_config("config.yaml")
    bodies = initialize_bodies(config)
    run_simulation(bodies, config)
    # input("press enter")

    return


if __name__ == "__main__":
    main()
