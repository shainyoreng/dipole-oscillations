
def save_csv(t, left, right, filename):
    requction_factor = 100
    t_reduced = t[::reduction_factor]
    left_reduced = left[::reduction_factor]
    right_reduced = right[::reduction_factor]
    # Save the data to a CSV file
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['time', 'left_theta', 'right_theta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i in range(len(t_reduced)):
            writer.writerow({'time': t_reduced[i], 'left_theta': left_reduced[i], 'right_theta': right_reduced[i]})
