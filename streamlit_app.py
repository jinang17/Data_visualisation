import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from sklearn.linear_model import LinearRegression
#Increase the size of "Application Title"
side = st.sidebar.radio("Application", ["Home", "Data", "About"])

if side == "Home":
    import streamlit as st

    # Define the available plot options
    plot_options = [
        "Efficiency Comparison of Devices",
        "Average RPM Comparison of Devices",
        "Maintenance Time Comparison of Devices",
        "Duration the device was OFF",
        "Total Rotations vs Time",
        f"Linear Regression - Device 1",
    ]

    # Create the dropdown to select the plot
    selected_plot = st.selectbox("Select a plot to display", plot_options)

    # Display the selected plot based on the dropdown selection
    if selected_plot == "Efficiency Comparison of Devices":
                # Read the CSV file
        data = pd.read_csv('dataset.csv')

        # Calculate the duty cycle for each device
        data['duty_cycle'] = data['On_time'] / (data['On_time'] + data['Off_time'])

        # Group the data by Device_id and calculate the average duty cycle
        grouped_data = data.groupby('Device_id')['duty_cycle'].mean()

        # Create the plot using matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(grouped_data)), grouped_data)
        ax.set_xlabel('Device ID')
        ax.set_ylabel('Duty Cycle')
        ax.set_title('Efficiency Comparison of Devices')
        ax.set_xticks(range(len(grouped_data)))
        ax.set_xticklabels(grouped_data.index, rotation=45, ha='right')  # Adjust rotation and alignment
        ax.grid(True)

        # Add labels for each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        # Display the plot using Streamlit
        st.pyplot(fig)
        pass

    elif selected_plot == "Average RPM Comparison of Devices":
                # Read the CSV file
        data = pd.read_csv('dataset.csv')

        # Convert time column to datetime if it's not already in datetime format
        data['time'] = pd.to_datetime(data['time'])

        # Calculate the average RPM for each device
        average_rpm = data.groupby('Device_id')['RPM'].mean()

        # Create the plot using matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(average_rpm.index, average_rpm)
        ax.set_xlabel('Device ID')
        ax.set_ylabel('Average RPM')
        ax.set_title('Average RPM Comparison of Devices')
        ax.set_xticks(average_rpm.index)
        ax.set_xticklabels(average_rpm.index, rotation=45, ha='right')  # Adjust rotation and alignment
        ax.grid(True)

        # Add labels for each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        # Display the plot using Streamlit
        st.pyplot(fig)
        pass

    elif selected_plot == "Maintenance Time Comparison of Devices":
        # Read the CSV file
        data = pd.read_csv('dataset.csv')

        # Calculate the maintenance time per 100 seconds for each device
        maintenance_time = data.groupby('Device_id')['Off_time'].sum() / 100

        # Create the plot using matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(maintenance_time.index, maintenance_time)
        ax.set_xlabel('Device ID')
        ax.set_ylabel('Maintenance Time (per 100 seconds)')
        ax.set_title('Maintenance Time Comparison of Devices')
        ax.set_xticks(maintenance_time.index)
        ax.set_xticklabels(maintenance_time.index, rotation=45, ha='right')  # Adjust rotation and alignment
        ax.grid(True)

        # Add labels for each bar
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords='offset points',
                        ha='center', va='bottom')

        # Display the plot using Streamlit
        st.pyplot(fig)

    elif selected_plot == "Duration the device was OFF":
        # Read the CSV file
        data = pd.read_csv('dataset.csv')

        # Get unique device IDs
        device_ids = data['Device_id'].unique()

        # Iterate over each device ID
        for device_id in device_ids:
            # Filter data for the current device ID
            device_data = data[data['Device_id'] == device_id]

            # Extract the 'Off_time' and 'time' columns
            off_time = device_data['Off_time']
            time = pd.to_datetime(device_data['time'])

            # Calculate the differences between consecutive 'Off_time' values and time differences
            off_time_diff = off_time.diff()
            time_diff = time.diff().dt.total_seconds() / 60.0

            # Calculate the slope as off_time_diff / time_diff
            slope = off_time_diff / time_diff

            # Create the plot using matplotlib
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(time, slope, color='red')
            ax.set_xlabel('Time')
            ax.set_ylabel('Duration the device was OFF')
            ax.set_title(f'Slope of Off Time vs Time - Device {device_id}')
            ax.set_ylim(0, 5)  # Set the Y-axis range as per your preference
            ax.grid(True)

            # Display the plot using Streamlit
            st.pyplot(fig)

    elif selected_plot == "Total Rotations vs Time":
             # Read the CSV file
            data = pd.read_csv('dataset.csv')

            # Convert time column to datetime if it's not already in datetime format
            data['time'] = pd.to_datetime(data['time'])

            # Group the data by Device_id
            grouped_data = data.groupby('Device_id')

            # Create a figure and axes for the plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Plot Total_rotations vs Time for each device
            for device_id, device_data in grouped_data:
                # Check for consistent On_time
                consistent_on_time = (device_data['On_time'].diff() == 0)

                # Plot the line
                ax.plot(device_data['time'], device_data['Total_rotations'], label='Device {}'.format(device_id))

                # Highlight the portion where On_time is consistent
                x = np.array(device_data['time'][consistent_on_time])
                y = np.array(device_data['Total_rotations'][consistent_on_time])
                ax.scatter(x, y, color='red', marker=",", s=20)

            
            plt.plot([], [], color='red', marker=',', markersize=5, label='Downtime')
            # Set the plot labels and title
            ax.set_xlabel('Time')
            ax.set_ylabel('Total Rotations')
            ax.set_title('Total Rotations vs Time')
            ax.legend()
            ax.grid(True)

            # Display the plot using Streamlit
            st.pyplot(fig)

    elif selected_plot.startswith("Linear Regression - Device"):
                    # Read the CSV file
            data = pd.read_csv('dataset.csv')

            # Get unique device IDs
            device_ids = data['Device_id'].unique()

            # Create a dropdown for device selection
            device_selection = st.selectbox('Select Device', device_ids)

            # Filter data for the selected device ID
            device_data = data[data['Device_id'] == device_selection]

            # Extract the total rotations and time columns
            total_rotations = device_data['Total_rotations']
            time = pd.to_datetime(device_data['time'])

            # Convert time to numeric values
            time_numeric = pd.to_numeric(time)

            # Reshape the time data to match the expected input shape for Linear Regression
            X = time_numeric.values.reshape(-1, 1)
            y = total_rotations.values

            # Create a Linear Regression model
            model = LinearRegression()

            # Fit the model to the data
            model.fit(X, y)

            # Predict the total rotations using the linear regression model
            predictions = model.predict(X)

            # Plot the actual data and the linear regression line
            plt.figure(figsize=(12, 6))
            plt.scatter(time, total_rotations, label='Actual Data')
            plt.plot(time, predictions, color='red', label='Linear Regression')
            plt.xlabel('Time')
            plt.ylabel('Total Rotations')
            plt.legend()
            plt.title(f'Linear Regression - Device {device_selection}')

            # Convert the Matplotlib figure to Streamlit format
            st.pyplot(plt)
            pass


elif side == "Data":
    st.title("Data")
    # Read the dataset into a DataFrame
    df = pd.read_csv("dataset.csv")
    # Display the DataFrame using Streamlit
    st.write(df)
    pass

elif side == "About":
    st.title("About Me")
    # Display name
    st.markdown("### Name")
    st.write("Jinang Vohera")

    #Display Bio 
    st.markdown("### Bio")
    st.write("I am a Computer Science student at Nirma University who likes to solve problems and build stuff using my coding skills . I am a life-long learner who is always eager to learn new things.")
    
    # Display email ID
    st.markdown("### Email ID")
    st.write("jinangsmiles17@gmail.com")
    # Display GitHub link
    st.markdown("### GitHub Link")
    st.write("[GitHub : jinang17 ](https://github.com/jinang17)")
    
    # Display LinkedIn link
    st.markdown("### LinkedIn Link")
    st.write("[LinkedIn : Jinang ](https://www.linkedin.com/in/jinang-vohera-a0174920a/)")

