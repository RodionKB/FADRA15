class RewardDistribution:
    def __init__(self, total_reward_pool, beta_min, beta_max, alpha_min, alpha_max, t_max, activity_average):
        self.total_reward_pool = total_reward_pool
        self.beta_min = beta_min
        self.beta_max = beta_max
        self.alpha_min = alpha_min
        self.alpha_max = alpha_max
        self.t_max = t_max
        self.activity_average = activity_average

    def calculate_reward(self, token_holding, proportional_share, holding_time, user_transactions, total_weighted_tokens):
        # Progressive Bonus (β)
        beta = self.beta_min + (self.beta_max - self.beta_min) * (1 - proportional_share)
        # Regressive Penalty (α)
        alpha = self.alpha_min + (self.alpha_max - self.alpha_min) * proportional_share
        # Holding Multiplier (H_holding)
        holding_multiplier = min(holding_time / self.t_max, 1)
        # Activity Multiplier (S_activity)
        activity_multiplier = user_transactions / self.activity_average
        # Weighted Tokens
        weighted_tokens = token_holding * (1 + beta - alpha) * (1 + holding_multiplier) * activity_multiplier
        # Reward Calculation
        reward = self.total_reward_pool * (weighted_tokens / total_weighted_tokens)
        # Apply minimum and maximum caps
        min_reward = 0.15 * self.total_reward_pool
        max_reward = 0.999 * self.total_reward_pool
        return max(min_reward, min(reward, max_reward))

# Example Usage
reward_system = RewardDistribution(
    total_reward_pool=10000,  # Total Reward Pool
    beta_min=0.05,           # Minimum Bonus
    beta_max=0.15,           # Maximum Bonus
    alpha_min=0.02,          # Minimum Penalty
    alpha_max=0.10,          # Maximum Penalty
    t_max=365,               # Maximum Holding Time (in days)
    activity_average=10      # Average Transactions Per User
)

# Sample data for a participant
token_holding = 1000
proportional_share = 0.02  # Participant's share
holding_time = 180  # Days
user_transactions = 12
total_weighted_tokens = 50000  # Sum of weighted tokens across all participants

reward = reward_system.calculate_reward(
    token_holding=token_holding,
    proportional_share=proportional_share,
    holding_time=holding_time,
    user_transactions=user_transactions,
    total_weighted_tokens=total_weighted_tokens
)

print(f"Calculated Reward: {reward}")
