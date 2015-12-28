from random import randint


def cluster(data, num_k):
    # take random 10 points
    means = list(map(
            lambda x: data[randint(0, len(data))],
            range(0, num_k)
    ))
    means.sort()

    return __cluster(means, data)


def __cluster(means_input, data):
    param = 0.01  # bigger numbers make the means change faster
    # must be between 0 and 1

    means = means_input

    for x in data:
        closest_k = 0
        smallest_error = 9999  # this should really be positive infinity
        for k in enumerate(means):
            error = abs(x - k[1])
            if error < smallest_error:
                smallest_error = error
                closest_k = k[0]
        means[closest_k] = means[closest_k] * (1 - param) + x * (param)

    def find_index_means(x):
        return 1 + min(range(0, len(means)), key=lambda i: abs(means[i] - x))

    indexes = list(map(find_index_means, data))
    means_corresponding = list(map(lambda x: means[x-1], indexes))
    return indexes, means_corresponding
