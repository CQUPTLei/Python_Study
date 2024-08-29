import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Assume transfer function data
numerators = [4, 2, 10, 10, 2, 4, 10, 10, 10, 9, 2, 10, 4]
denominators = [
    [1, 2, 0], [1, 10, 0], [1, 9, 0], [1, 2, 11], [1, 0.5, 0],
    [1, 2, 0], [1, 1.6, 4], [1, 5, 24], [1, 2.5, 24], [1, 2, 9],
    [1, 0.25, 0], [1, 5, 4], [1, 0.15, 0]
]
H_values = [10, 10, 5, 1, 1, 1, 5, 3, 1, 1, 0.5, 5, 10]
Kp_values = [
    [1, 5, 10], [1, 4, 10], [1, 4, 10], [1, 10, 100], [0.1, 1, 10],
    [0.5, 5, 50], [1, 10, 50], [2, 20, 200], [1, 25, 250], [1, 25, 250],
    [0.2, 20, 200], [1, 10, 50], [1, 5, 10]
]

results = []

# Generate 13 step response plots, each containing 3 different Kp values
for i in range(13):
    G1 = ctrl.TransferFunction(numerators[i], denominators[i])
    H = H_values[i]
    plt.figure()

    for Kp in Kp_values[i]:
        G_OL = Kp * G1
        T = ctrl.feedback(G_OL, H)
        t, y = ctrl.step_response(T)

        # Calculate performance metrics
        info = ctrl.step_info(T)
        max_overshoot = info['Overshoot']
        rise_time = info['RiseTime']
        settling_time = info['SettlingTime']
        steady_state_error = abs(1 - y[-1])  # Error at final value

        poles = np.roots(denominators[i])
        zeta = []
        omega_n = []

        for pole in poles:
            if np.abs(pole) != 0:
                zeta.append(-np.real(pole) / np.abs(pole))
                omega_n.append(np.abs(pole))
            else:
                zeta.append(np.nan)  # Unable to calculate damping ratio
                omega_n.append(np.nan)  # Unable to calculate undamped natural frequency

        # Record results
        results.append({
            'System': i + 1,
            'Kp': Kp,
            'Rise Time (tr)': rise_time,
            'Settling Time (ts)': settling_time,
            'Maximum Overshoot (%)': max_overshoot,
            'Steady State Error': steady_state_error,
            'Damping Ratio (zeta)': zeta[0] if len(zeta) > 0 else 'N/A',
            'Undamped Natural Frequency (omega_n)': omega_n[0] if len(omega_n) > 0 else 'N/A'
        })

        plt.plot(t, y, label=f"Kp={Kp}")

    plt.xlabel('Time (s)')
    plt.ylabel('Response')
    plt.title(f'Step Response of System {i + 1}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'step_response_system_{i + 1}.png')
    # plt.show()
    plt.close()

# Save results to an Excel file
df = pd.DataFrame(results)
df.to_excel('step_response_results.xlsx', index=False)

print("All data has been calculated and saved to step_response_results.xlsx")
