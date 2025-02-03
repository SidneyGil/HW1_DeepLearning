from typing import Tuple

import torch


class WeatherForecast:
    def __init__(self, data_raw: list[list[float]]):
        """
        You are given a list of 10 weather measurements per day.
        Save the data as a PyTorch (num_days, 10) tensor,
        where the first dimension represents the day,
        and the second dimension represents the measurements.
        """
        self.data = torch.as_tensor(data_raw, dtype=torch.float32).view(-1, 10)

    def find_min_and_max_per_day(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Find the max and min temperatures per day

        Returns:
            min_per_day: tensor of size (num_days,)
            max_per_day: tensor of size (num_days,)
        """
        return self.data.min(dim=1).values, self.data.max(dim=1).values


    def find_the_largest_drop(self) -> torch.Tensor:
        """
        Find the largest change in day over day average temperature.
        This should be a negative number.

        Returns:
            tensor of a single value, the difference in temperature
        """
        return torch.diff(self.data.mean(dim=1)).min()


    def find_the_most_extreme_day(self) -> torch.Tensor:
        """
        For each day, find the measurement that differs the most from the day's average temperature

        Returns:
            tensor with size (num_days,)
        """
        # Utilized Copilot: finds how far each temperature measurements deviates from the daily mean
        deviations = (self.data - self.data.mean(dim=1, keepdim=True)).abs()
        # Returns the temperature measurement with the highest deviation per day by utilizing the deviations variable:
        #   deviations.argmax(dim=1, keepdim=True): Finds the index of the largest deviation in each day's data.
        #   self.data.gather(dim=1, index=...): Retrieves the corresponding temperature values from `self.data`.
        #   .squeeze(): Removes extra dimensions to return a 1D tensor of most extreme measurements.
        return self.data.gather(dim=1, index=deviations.argmax(dim=1, keepdim=True)).squeeze() # 


    def max_last_k_days(self, k: int) -> torch.Tensor:
        """
        Find the maximum temperature over the last k days

        Returns:
            tensor of size (k,)
        """
        return self.data[-k:].max(dim=1).values

    def predict_temperature(self, k: int) -> torch.Tensor:
        """
        From the dataset, predict the temperature of the next day.
        The prediction will be the average of the temperatures over the past k days.

        Args:
            k: int, number of days to consider

        Returns:
            tensor of a single value, the predicted temperature
        """
        return self.data[-k:].mean(dim=1).mean()


    def what_day_is_this_from(self, t: torch.FloatTensor) -> torch.LongTensor:
        """
        You go on a stroll next to the weather station, where this data was collected.
        You find a phone with severe water damage.
        The only thing that you can see in the screen are the
        temperature reading of one full day, right before it broke.

        You want to figure out what day it broke.

        The dataset we have starts from Monday.
        Given a list of 10 temperature measurements, find the day in a week
        that the temperature is most likely measured on.

        We measure the difference using 'sum of absolute difference
        per measurement':
            d = |x1-t1| + |x2-t2| + ... + |x10-t10|

        Args:
            t: tensor of size (10,), temperature measurements

        Returns:
            tensor of a single value, the index of the closest data element
        """
        return (self.data - t).abs().sum(dim=1).argmin() # copilot used to fix error, but idea was there
