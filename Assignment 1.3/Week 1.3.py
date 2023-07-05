# Importing libraries
import matplotlib.pyplot as plt
import linecache
import time


class CsvConverter:
    """
    This is a class for converting a csv file into a json file. 
    
    Attributes:
        file_path: A string indicating the path to the csv file.
        header_line: The list of keys (header) in the csv file.
    """
    def __init__(self, file_path): 
        self.file_path = file_path
        # Reading the first line of file which contains headers for CSV.
        self.header_line = linecache.getline(self.file_path, 1).strip('\n').split(',')

    def csv_to_json(self, list_lines):
        """
        The function to convert the csv file into a json file.

        Args:
            list_lines: A list of strings, where each string is a line from a CSV file

        Returns:
            result: A list of dictionaries, where each dictionary represents a line from 
                    the CSV file, with keys being the header names and values being the data 
                    from the line.                    
        """
        result = [] 
        for line in list_lines: 
            line_data = line.strip('\n').split(',')
            # Checking if the line data and header have the same length
            if len(line_data) == len(self.header_line):
                # Creating a dictionary from line data and header
                line_dict = dict(zip(self.header_line, line_data))  
                # Adding the dictionary to the result list
                result.append(line_dict)  

        return result


class Reader:
    """
    Reader class for reading data from a CSV file.

    This class provides a reader that can read data from a CSV file in a stride manner
    and notifies its observers every time new data is read. 
    
    Attributes:
        file_path: A string indicating the path to the csv file.
        stride: An integer indicating the number of lines to be read in each read operation. 
        header_line: A list of strings representing the headers of the CSV file.
        start_line: An integer representing the line number from where to start reading.
        observers: A set to hold observer objects that need to be notified when new data is read.

    Methods:
        add_observer(observer): Adds an observer to the set of observers.
        remove_observer(observer): Removes an observer from the set of observers.
        notify_observers(data): Notifies all observers that new data has been read.
        get_lines(): Reads the next stride of lines from the data, notifies the observers, 
                     and returns the data in JSON format.
        start_reading(): Starts reading the CSV file line by line, each time reading a number of
                         lines equal to the stride. It waits for 5 seconds after each read operation.             
    """
    def __init__(self, file_path='dSST.csv', stride=5):
        """
        Initializes a new instance of the Reader class.

        Args:
            file_path: A string indicating the path to the csv file.
            stride: An integer indicating the number of lines to be read in each read operation.
        """
        self.file_path = file_path
        self.stride = stride
        self.header_line = linecache.getline(self.file_path, 1).strip('\n').split(',')
        self.start_line = 2
        self.observers = set()

    def add_observer(self, observer):
        """
        Adds an observer to the set of observers.

        Args:
            observer: The observer to be added.
        """
        self.observers.add(observer)

    def remove_observer(self, observer):
        """
        Removes an observer from the set of observers.

        Args:
            observer: The observer to be removed.
        """
        self.observers.remove(observer)

    def notify_observers(self, data):
        """
        Notifies all observers that new data has been read.

        Args:
            data: the newly read data
        """
        for observer in self.observers:
            observer.update(data)

    def get_lines(self):
        """
        Reads the next stride of lines from the data, notifies the observers, 
        and returns the data in JSON format.

        Returns:
            A string containing the data in JSON format.
        """
        line_list = []
        # Read 'stride' number of lines from the CSV file starting from 'start_line'
        for i in range(self.stride):
            line = linecache.getline(self.file_path, self.start_line + i)
            # Append each line read to 'line_list'
            line_list.append(line)

        # Filter out any empty lines from 'line_list'
        non_empty_lines = [line for line in line_list if line.strip() != '']

        # If there are non-empty lines, convert them to JSON format and notify observers
        if non_empty_lines:
            result = CsvConverter(self.file_path).csv_to_json(non_empty_lines)
            self.start_line += self.stride 
            self.notify_observers(result)
            return result
        else:
            return ''

    def start_reading(self):
        """
        Start reading the CSV file line by line in strides until there are no more lines to read.  
        """
         
        while True:
            # Fetch 'stride' number of lines from the CSV file and if end of file is reached break the loop
            lines = self.get_lines() 
            if lines == '':
                break
            
            # Pause for 5 seconds before fetching the next set of lines
            time.sleep(5)




class AverageYear:
    
    """
    The AverageYear class is responsible for calculating and visualizing the average temperature 
    anomaly for each year. The class stores the calculated averages and corresponding years, and generates 
    a line plot visualizing the average temperature anomaly each year.

    Attributes:
        years: A list storing the number of years that have passed since the first data.
        temperatures: A list storing the calculated average temperature anomalies.
        figure: A matplotlib figure object used for plotting.
        ax: A matplotlib axes object used for plotting.

    Methods:
        update(data): Updates the years and temperatures attributes with the newly calculated 
                      average temperature and increments the year count.
        ave_temp(data): Calculates the average temperature anomaly from the given data.
        ave_plotter(): Plots the calculated average temperature anomalies against the number of 
                       years passed since the first data.
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the AverageYear object.This method initializes 
        the years and temperatures attributes as empty lists. It also creates a figure and an axes
        object for plotting.
        """
        self.years = []
        self.temperatures = []
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot( )

    def update(self, data):
        """
        Update the years, temperatures, and plot with new data. 

        Args:
            data: A list of dictionaries, where each dictionary represents a line from the CSV file,
                  with keys as column headers and values as column values. 
        """
        avg = self.ave_temp(data)
        if avg:
            self.years.append(len(self.years) + 1)
            self.temperatures.append(avg)
            self.ave_plotter()

    def ave_temp(self, data):
        """
        Calculate the average temperature for the given data. 

        Args:
            data: A list of dictionaries, where each dictionary represents a line from the CSV file, 
                  with keys as column headers and values as column values.

        Returns:
            The calculated average temperature as a float number, or None if the data is empty.
        """
        count = len(data)
        sum_temp = sum(float(line['J-D']) for line in data)
        if count == 0:
            return None
        avg = sum_temp /count
        return avg

    def ave_plotter(self):
        """
        This method clears the current plot, plots the average temperature against the years on a 
        line graph, and sets the x-axis label, y-axis label, title, and grid for the plot.
        """ 
        self.ax.clear()
        self.ax.plot(self.years, self.temperatures, 'bo-')
        self.ax.set_xlabel('Year')
        self.ax.set_ylabel('Average Temperature')
        self.ax.set_title('Average Yearly Temperature')
        self.ax.grid(True)
        plt.pause(0.01)



 
class AverageMonth:
    """
    The AverageMonth class calculates and stores averages for each month and year, and generates 
    line plots visualizing the average temperature anomaly for each month and each year.

    Attributes:
        months: A list of string representing each month.
        monthly_averages: A dictionary storing the calculated average temperature anomalies for each month.
        years: A list storing the number of years that have passed since the first data.
        yearly_averages: A list storing the calculated average temperature anomalies for each year.
        monthly_figure: A matplotlib figure object used for plotting the monthly averages.
        monthly_ax: A matplotlib axes object used for plotting the monthly averages.
        yearly_figure: A matplotlib figure object used for plotting the yearly averages.
        yearly_ax: A matplotlib axes object used for plotting the yearly averages.

    Methods:
        update(data): Updates the monthly_averages and yearly_averages attributes with the newly 
                      calculated averages, and increments the year count.
        ave_temp(data): Calculates the average temperature anomaly from the given data and adds it 
                        to the yearly_averages list. Also adds the monthly anomalies to the monthly_averages
                        dictionary.
        monthly_ave_plotter(): Plots the calculated average temperature anomalies for each month against
                               the number of years passed since the first data.
        yearly_ave_plotter(): Plots the calculated average temperature anomalies for each year against
                              the number of years passed since the first data.
    """
    def __init__(self):
        """
        Initializes an AverageMonth object. 
        """
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.monthly_averages = {month: [] for month in self.months}
        self.years = []
        self.yearly_averages = []
        self.monthly_figure, self.monthly_ax = plt.subplots()
        self.yearly_figure, self.yearly_ax = plt.subplots()

    def update(self, data):
        """
        This method is called when new data is received. It calculates the average temperature 
        for the given data using the 'ave_temp' method. It then updates the monthly and yearly 
        average plots using the calculated averages.

        Args:
            data: A list of dictionaries, where each dictionary represents a line from the CSV file, 
                  with keys as column headers and values as column values.
        """
        self.ave_temp(data)
        self.monthly_ave_plotter()
        self.yearly_ave_plotter()

    def ave_temp(self, data):
        """
        This method calculates the average temperature by summing the 'J-D' values from the data
        and dividing it by the count of data points. If the count is zero, indicating empty data, 
        None is returned. It adds the yearly average to the yearly_averages list and adds the monthly 
        averages to the monthly_averages dictionary.

        Args:
            data: A list of dictionaries, where each dictionary represents a line from the CSV file, 
                  with keys as column headers and values as column values.
        """
        count = len(data)
        sum_temp = sum(float(line['J-D']) for line in data)
        if count == 0:
            return None
        avg = sum_temp / count
        # Append the current year count to the years list
        self.years.append(len(self.years) + 1)

        # Append the calculated average to the yearly averages list
        self.yearly_averages.append(avg)

        # Append the monthly average temp to the corresponding month in the monthly averages dictionary 
        for month in self.months:
            self.monthly_averages[month].append(float(data[0][month]))

    def monthly_ave_plotter(self):
        """
        This method clears the current plot and plots the average temperature anomalies for each
        month against the number of data points. It sets the x-axis label, y-axis label, title, legend, 
        and grid for the plot.
        """
        self.monthly_ax.clear()

        # Plot the average temperature anomalies for each month
        for month, temps in self.monthly_averages.items():
            self.monthly_ax.plot(range(1, len(temps) + 1), temps, label=month)

        self.monthly_ax.set_xlabel('Data')
        self.monthly_ax.set_ylabel('Average Temperature')
        self.monthly_ax.set_title('Monthly Average')
        self.monthly_ax.legend()
        self.monthly_ax.grid(True)
        plt.pause(0.01)

    def yearly_ave_plotter(self):
        """
        This method clears the current plot and plots the average temperature anomalies for each year 
        against the number of years passed since the first data. It sets the x-axis label, y-axis label, 
        title, and grid for the plot.
        """
        self.yearly_ax.clear()
        self.yearly_ax.plot(self.years, self.yearly_averages, 'bo-')
        self.yearly_ax.set_xlabel('Year')
        self.yearly_ax.set_ylabel('Average Temperature')
        self.yearly_ax.set_title('Yearly Average')
        self.yearly_ax.grid(True)
        plt.pause(0.01)



# Testing code
reader = Reader('dSST.csv')
average_month = AverageMonth()
reader.add_observer(average_month)
reader.start_reading()
