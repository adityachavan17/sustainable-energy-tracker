from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def generate_plot():
    try:
        df = pd.read_csv('energy_data.csv')
        country = 'India'
        country_data = df[df['Entity'] == country].dropna(subset=['Primary energy consumption per capita (kWh/person)'])
        
        if country_data.empty:
            return None, f"No data for {country}"
        
        years = country_data['Year']
        energy_per_capita = country_data['Primary energy consumption per capita (kWh/person)']
        
        plt.figure(figsize=(10, 5))
        plt.plot(years, energy_per_capita, marker='o')
        plt.title(f'Energy Usage Per Capita in {country}')
        plt.xlabel('Year')
        plt.ylabel('kWh per Person')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plot_path = 'static/energy_plot.png'
        plt.savefig(plot_path)
        plt.close()
        
        avg_usage = energy_per_capita.mean()
        latest_usage = energy_per_capita.iloc[-1]
        tip = ("Reduce energy waste: Use LED bulbs and unplug devices."
               if latest_usage > avg_usage else "Good job maintaining low energy use!")
        
        return plot_path, tip
    except Exception as e:
        return None, f"Error: {str(e)}"

@app.route('/')
def home():
    plot_path, tip = generate_plot()
    if plot_path is None:
        return f"Error: {tip}"
    return render_template('index.html', plot_url=plot_path, tip=tip)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
