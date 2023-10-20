def read_data(filename):
    # TODO) Read `filename` as a list of integer numbers
    # DONE
    data = []
    lines = open(filename).read().splitlines()
    for line in lines:
        data.append(line.split(', '))
    data.remove(data[0])

    for da in data:
        for d in da:
            d = int(d)

    return data

def calc_weighted_average(data_2d, weight):
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    for data in data_2d:
        average.append(int(data[0])*float(weight[0]) + int(data[1])*float(weight[1]))
    return average

def analyze_data(data_1d):
    # TODO) Derive summary of the given `data_1d`
    # Note) Please don't use NumPy and other libraries. Do it yourself.
    data_1d = list(map(float, data_1d))
    sum = 0
    for data in data_1d:
        sum = sum + int(data)

    mean = sum/len(data_1d)

    square = 0
    for data in data_1d:
        square = square + int(data)**2
    var = square/len(data_1d) - mean**2

    data_1d.sort()
    median = float(data_1d[int(len(data_1d)/2)])

    _min = float(min(data_1d))
    _max = float(max(data_1d))

    return mean, var, median, _min, _max

if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Total |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')

            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')