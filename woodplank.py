import random
import numpy as np

class PetriNetSimulation:
    def __init__(self):
        # Initialize places with tokens
        self.places = {
            'Production': 1,
            'Buffer1': 0,
            'Tool': 1,
            'Buffer2': 0,
            'Buffer3': 0,
            'ToolOccupied': 0,
            'PostProcessing': 0
        }
        self.tool_unavailable_duration = 0

    def produce(self):
        # Simulate production step
        if self.places['Production'] > 0:
            self.places['Production'] -= 1
            self.places['Buffer1'] += 1

    def work_on_item(self):
        # Simulate working on item if tool is available
        if self.places['Tool'] > 0 and self.places['Buffer1'] > 0:
            self.places['Tool'] -= 1
            self.places['Buffer1'] -= 1
            self.places['Buffer2'] += 1
            self.places['ToolOccupied'] += 1

    def release_tool(self):
        # Simulate tool release after work
        if self.places['ToolOccupied'] > 0:
            self.places['ToolOccupied'] -= 1
            self.places['Tool'] += 1

    def post_process(self):
        # Simulate post-processing
        if self.places['Buffer2'] > 0:
            self.places['Buffer2'] -= 1
            self.places['PostProcessing'] += 1

    def complete_post_processing(self):
        # Simulate completion of post-processing
        if self.places['PostProcessing'] > 0:
            self.places['PostProcessing'] -= 1
            self.places['Buffer3'] += 1
            self.places['Production'] += 1  # Assuming a cyclic process

    def simulate_step(self):
        self.produce()
        self.work_on_item()
        self.release_tool()
        self.post_process()
        self.complete_post_processing()

        # Check for tool unavailability
        if random.random() < 0.1:  # Assume 10% chance the tool is not available
            self.tool_unavailable_duration += 1
            self.places['Tool'] = 0
        else:
            if self.tool_unavailable_duration > 0:
                self.places['Tool'] = 1
                self.tool_unavailable_duration = 0

    def run_simulation(self, num_steps):
        for _ in range(num_steps):
            self.simulate_step()

        # Return the state of the buffers and tool unavailability
        return self.places['Buffer2'], self.places['Buffer3'], self.tool_unavailable_duration

# Run Monte Carlo simulation
num_runs = 1000
buffer2_sizes = []
buffer3_sizes = []
tool_unavailable_durations = []

for _ in range(num_runs):
    sim = PetriNetSimulation()
    buffer2, buffer3, tool_unavailable_duration = sim.run_simulation(1000)
    buffer2_sizes.append(buffer2)
    buffer3_sizes.append(buffer3)
    tool_unavailable_durations.append(tool_unavailable_duration)

# Analyze results
print(f"Average size of Buffer2: {np.mean(buffer2_sizes)}")
print(f"Average size of Buffer3: {np.mean(buffer3_sizes)}")
print(f"Average tool unavailable duration: {np.mean(tool_unavailable_durations)}")