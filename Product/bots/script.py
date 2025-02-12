import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

from bot import Bot
from sql_data_service import SqlDataService

random.seed(42)
np.random.seed(42)

def generate_distribution(min_val, max_val, a, b, name):

    samples = beta.rvs(a = a, b = b, size=10000)
    distribution = min_val + (max_val - min_val) * samples

    # scaled_data = min_val + (max_val - min_val) * samples
    # integer_data = np.round(scaled_data).astype(int)
    # distribution = np.clip(integer_data, min_val, max_val)

    plt.hist(distribution, bins=max_val - min_val + 1, edgecolor='k', color='tab:orange')
    plt.title(f'Distribution {name}')
    plt.xlabel('Watch Percentage')
    plt.ylabel('Density')
    plt.savefig(f'distributions/{name}.png')
    plt.clf()

    return distribution


class Distributions():
    def __init__(self):
        self.d1 = generate_distribution(0, 100, 3.5, 32, 'level_1')
        self.d2 = generate_distribution(0, 100, 27, 63, 'level_2')
        self.d3 = generate_distribution(0, 100, 54, 54,  'level_3')
        self.d4 = generate_distribution(0, 100, 63, 27, 'level_4')
        self.d5 = generate_distribution(0, 100, 32, 3.5, 'level_5')
    
    def plot_all_distributions(self):
        plt.hist(self.d1, bins=100, alpha=0.7, label='level_1', color='tab:orange')
        plt.hist(self.d2, bins=100, alpha=0.7, label='level_2', color='tab:blue')
        plt.hist(self.d3, bins=100, alpha=0.7, label='level_3', color='tab:green')
        plt.hist(self.d4, bins=100, alpha=0.7, label='level_4', color='tab:red')
        plt.hist(self.d5, bins=100, alpha=0.7, label='level_5', color='tab:purple')
        plt.ylim(0, 500)
        
        plt.title('All Distributions')
        plt.xlabel('Watch Percentage')
        plt.ylabel('Density')
        plt.legend(loc='upper right')
        plt.savefig('distributions/all_distributions.png')
        plt.clf()

def main(nr_bots):
    # Setting classes
    classes = ['biology chemistry', 'arts literature music psychology', 'business literature', 'mathematics physics', 'biology chemistry psychology', 'computer_science physics', 'biology chemistry mathematics physics', 'computer_science mathematics physics', 'business psychology', 'literature psychology', '']

    percentages = [0.02, 0.08, 0.20, 0.13, 0.12, 0.04, 0.04, 0.20, 0.04, 0.06, 0.07]

    # Generating distributions:
    distributions = Distributions()
    distributions.plot_all_distributions()


    failed_bots = 0
    bots = []
    for i in range(nr_bots):
        categories = random.choices(classes, weights=percentages, k=1)[0]

        if categories == '':
            failed_bots += 1
            continue    

        levels = [random.randint(2, 5) for c in categories.split(' ')]
        bot = Bot(i + 1, categories.split(' '), levels)
        bot.generate_vector()

        # Inserting created bots into db
        data_service = SqlDataService()

        # check if bot is already introduced
        username = f'bot{bot.bot_id}'
        usernames = data_service.get_usernames()
        if not username in usernames:
            print(bot.vector)
            data_service.insert_bot(bot)

        bots.append(bot)

    for bot in bots:
        if bot.create_account() != 0:
            continue
        if bot.log_in() != 0:
            continue

        video_list = bot.request_videos()
        while video_list != []:
            for video in video_list:
                # print(video)
                # For videos with multiple categories
                weighted_sum = 0
                sum_weights = 0
                for category in video['categories'].split(' '):
                    interest_level = bot.categories[category]
                    watch_percentage = 0
                    if interest_level == 1:
                        watch_percentage = int(np.random.choice(distributions.d1))
                    elif interest_level == 2:
                        watch_percentage = int(np.random.choice(distributions.d2))
                    elif interest_level == 3:
                        watch_percentage = int(np.random.choice(distributions.d3))
                    elif interest_level == 4:
                        watch_percentage = int(np.random.choice(distributions.d4))
                    elif interest_level == 5:
                        watch_percentage = int(np.random.choice(distributions.d5))
                    weighted_sum += interest_level * watch_percentage
                    sum_weights += interest_level
                avg_weighted_watch_percentage = weighted_sum // sum_weights

                # # For videos with single category
                # category = video['categories']
                # interest_level = bot.categories[category]
                # avg_weighted_watch_percentage = 0
                # if interest_level == 1:
                #     avg_weighted_watch_percentage = int(np.random.choice(distributions.d1))
                # elif interest_level == 2:
                #     avg_weighted_watch_percentage = int(np.random.choice(distributions.d2))
                # elif interest_level == 3:
                #     avg_weighted_watch_percentage = int(np.random.choice(distributions.d3))
                # elif interest_level == 4:
                #     avg_weighted_watch_percentage = int(np.random.choice(distributions.d4))
                # elif interest_level == 5:
                #     avg_weighted_watch_percentage = int(np.random.choice(distributions.d5))

                action_type = 'like'
                if avg_weighted_watch_percentage < 75:
                    classes = ['like', '']
                    percentages = [0.75, 0.25]
                    action_type = random.choices(classes, weights=percentages, k=1)[0]
                if avg_weighted_watch_percentage < 50:
                    classes = ['like', '']
                    percentages = [0.50, 0.50]
                    action_type = random.choices(classes, weights=percentages, k=1)[0]
                if avg_weighted_watch_percentage < 25:
                    classes = ['', 'dislike']
                    percentages = [0.998, 0.002]
                    action_type = random.choices(classes, weights=percentages, k=1)[0]
                watch_time = avg_weighted_watch_percentage * int(video['duration']) // 100

                payload = {
                    'video_id': video['video_id'],
                    'action_type': action_type,
                    'duration': watch_time
                }
                # print(payload)
                bot.send_data(payload)
            video_list = bot.request_videos()
    
main(1)
