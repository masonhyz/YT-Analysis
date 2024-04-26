from wrangling import videos, channels
from scipy.stats import ttest_ind, shapiro, levene


def perform_tests(test_sample, control_sample):
    # Check for normality
    stat, p = shapiro(test_sample)
    print(f"Normality test for views on for test: Stat={stat:.3f}, P-value={p:.3e}")
    stat, p = shapiro(control_sample)
    print(f"Normality test for views on for control: Stat={stat:.3f}, P-value={p:.3e}")

    # Check for equal variances
    stat, p = levene(test_sample, control_sample)
    print(f"Levene's test for equal variances: Stat={stat:.3f}, P-value={p:.3e}")

    # T-test
    stat, p = ttest_ind(test_sample, control_sample, equal_var=True)
    print(f"T-test: Stat={stat:.3f}, P-value={p:.3e}")



if __name__ == "__main__":
    for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
        test_sample = videos[videos['publishDay'] == day]['loggedViews']
        control_sample = videos[videos['publishDay'] != day]['loggedViews']
        print(f"\nTesting if logged views are significantly different for videos published on {day}:")
        perform_tests(test_sample, control_sample)

    for length in ['Short', 'Medium', 'Long']:
        test_sample = videos[videos['durationCategory'] == length]['loggedViews']
        control_sample = videos[videos['durationCategory'] != length]['loggedViews']
        print(f"\nTesting logged views are significantly different for {length} length videos:")
        perform_tests(test_sample, control_sample)

    for status in [True, False]:
        test_sample = videos[videos['caption'] == status]['loggedViews']
        control_sample = videos[videos['caption'] != status]['loggedViews']
        print(f"\nTesting logged views are significantly different for captioned videos:")
        perform_tests(test_sample, control_sample)

