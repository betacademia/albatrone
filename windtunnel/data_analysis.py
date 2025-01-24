import matplotlib.pyplot as plt
from lmfit import models

# Data for plotting
angles = [0, 5, 10, 15, 20, 25]
lift_low = [50, 80, 100, 160, 195, 190]
lift_high = [60, 110, 140, 180, 200, 200]

lift_central = []
lift_error = []
for low, high in zip(lift_low, lift_high):
    lift_central.append((low + high) / 2)
    lift_error.append((high - low) / 2)

# Plotting
plt.errorbar(angles, lift_central, yerr=lift_error, fmt="o")
plt.xlabel("Angle of attack (degrees)")
plt.ylabel("Lift (N)")
plt.title("Lift vs angle of attack")
plt.savefig("measurements.png")
plt.show()


# Model
def function_lift(angle, a, b):
    return a * angle + b


# gewichten en error
N_inv_err = [1 / item for item in lift_error]

ons_model = models.Model(function_lift)
parameters = ons_model.make_params(a=0, b=0)
result = ons_model.fit(lift_central, angle=angles, params=parameters, weights=N_inv_err)

print(result.fit_report())

# Plotting
plt.errorbar(angles, lift_central, yerr=lift_error, fmt="o")
plt.plot(angles, result.best_fit)
plt.xlabel("Angle of attack (degrees)")
plt.ylabel("Lift (N)")
plt.title("Lift vs angle of attack")
plt.savefig("measurements_fit.png")
plt.show()
