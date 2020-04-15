from pyspark import SparkContext

sc = SparkContext()

show_views_file = sc.textFile('/user/cloudera/input/join2_gennum?.txt')

print(show_views_file.take(2))

def split_show_views(line):
    tokens = line.split(',')
    show = tokens[0]
    views = int(tokens[1])
    return (show, views)

show_views = show_views_file.map(split_show_views)

show_channel_file = sc.textFile('/user/cloudera/input/join2_genchan?.txt')


def split_show_channel(line):
    tokens = line.split(',')
    show = tokens[0]
    channel = tokens[1]
    return (show, channel)


show_channel = show_channel_file.map(split_show_channel)

joined_dataset = show_views.join(show_channel_file)

accum = sc.accumulator(0)

def viewers_channel_accumulate(show_viewers_channel):
    show = show_viewers_channel[0]
    tokens = show_viewers_channel[1]
    viewers = tokens[0]
    channel = tokens[1]
    if channel == 'BAT':
        accum.add(viewers)

joined_dataset.foreach(viewers_channel_accumulate)

print(accum.value)