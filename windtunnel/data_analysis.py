import matplotlib.pyplot as plt
from lmfit import models

# Data for plotting for the lift and drag measurements
angles = [0, 5, 10, 15, 20, 25]
lift_low = [50, 80, 100, 160, 195, 190]
lift_high = [60, 110, 140, 180, 200, 200]
drag_low = [20, 30, 35, 55, 70, 75]
drag_high = [25, 40, 45, 60, 80, 85]

lift_central = []
lift_error = []
drag_central = []
drag_error = []
for l_low, l_high, d_low, d_high in zip(lift_low, lift_high, drag_low, drag_high):
    lift_central.append((l_low + l_high) / 2)
    lift_error.append((l_high - l_low) / 2)
    drag_central.append((d_low + d_high) / 2)
    drag_error.append((d_high - d_low) / 2)

# Plotting the measurements
plt.errorbar(angles, lift_central, yerr=lift_error, fmt="bo", label="Lift")
plt.errorbar(angles, drag_central, yerr=drag_error, fmt="go", label="Drag")
plt.xlabel("Angle of attack (degrees)")
plt.ylabel("Lift (N)")
plt.xlim(-1, 27)
plt.ylim(0, 225)
plt.legend()
plt.title("Lift and drag vs angle of attack")
plt.savefig("measurements.png")
plt.show()


# model applied to the data
def function_lift(angle, a, b):
    return a * angle + b


L_inv_err = [1 / item for item in lift_error]
D_inv_err = [1 / item for item in drag_error]

lift_model = models.Model(function_lift)
lift_parameters = lift_model.make_params(a=0, b=0)
lift_result = lift_model.fit(
    lift_central, angle=angles, params=lift_parameters, weights=L_inv_err
)

drag_model = models.Model(function_lift)
drag_parameters = drag_model.make_params(a=0, b=0)
drag_result = drag_model.fit(
    drag_central, angle=angles, params=drag_parameters, weights=D_inv_err
)

# print("Lift fit results:" + lift_result.fit_report())
print("Drag fit results:" + drag_result.fit_report())

# Plotting
plt.errorbar(angles, lift_central, yerr=lift_error, fmt="bo")
plt.plot(angles, lift_result.best_fit, label="Lift fit")
plt.errorbar(angles, drag_central, yerr=drag_error, fmt="go")
plt.plot(angles, drag_result.best_fit, label="Drag fit")
plt.xlabel("Angle of attack (degrees)")
plt.ylabel("Lift (N)")
plt.xlim(-1, 27)
plt.ylim(0, 225)
plt.legend()
plt.title("Lift and drag vs angle of attack with fit")
plt.savefig("measurements_fit.png")
plt.show()
