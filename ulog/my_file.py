import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np


def load_and_align(alt_path, vel_path):
    alt_data = pd.read_csv(alt_path)
    vel_data = pd.read_csv(vel_path)

    alt_data['time'] = (alt_data['%time'] - alt_data['%time'].iloc[0]) / 1e9
    vel_data['time'] = (vel_data['%time'] - vel_data['%time'].iloc[0]) / 1e9

    alt_data = alt_data.sort_values(by="time")
    vel_data = vel_data.sort_values(by="time")

    merged_df = pd.merge_asof(
    alt_data, 
    vel_data, 
    on='time', 
    direction='nearest',
    tolerance= 2.5
)
    merged_df = merged_df[[ 'time', 'field.data','field.twist.linear.x',
       'field.twist.linear.y', 'field.twist.linear.z', 'field.twist.angular.x',
       'field.twist.angular.y', 'field.twist.angular.z'
]]
    merged_df = merged_df.rename(columns={
    'time': 'time_sec',
    'field.data': 'altitude',
    'field.twist.linear.x': 'vx',
    'field.twist.linear.y': 'vy',
    'field.twist.linear.z': 'vz',
    'field.twist.angular.x': 'ang_x',
    'field.twist.angular.y': 'ang_y',
    'field.twist.angular.z': 'ang_z'
})
 
    return merged_df


def fit_pca(normal_df, n_components):
    normal_df = normal_df.iloc[:,1:]
    scaler = StandardScaler()
    normal_df = scaler.fit_transform(normal_df)
    pca = PCA(n_components=n_components) 
    pca.fit(normal_df)
    return scaler, pca


def compute_anomaly_score(failure_df, scaler1, pca1):   
    failure_signals = failure_df.iloc[:,1:]
    scaled_failure_df = scaler1.transform(failure_signals)
    pca_x = pca1.transform(scaled_failure_df)
    X_reconstructed = pca1.inverse_transform(pca_x)
    squared_diff = (scaled_failure_df - X_reconstructed) ** 2
    total_error = np.sum(squared_diff, axis=1)
    return total_error


if __name__ == "__main__":
    alt_normal = 'C:/Users/deepz/Downloads/ulog/processed/processed/carbonZ_2018-10-05-14-34-20_1_no_failure/carbonZ_2018-10-05-14-34-20_1_no_failure-mavros-global_position-rel_alt.csv'
    vel_normal = 'C:/Users/deepz/Downloads/ulog/processed/processed/carbonZ_2018-10-05-14-34-20_1_no_failure/carbonZ_2018-10-05-14-34-20_1_no_failure-mavros-local_position-velocity.csv'

    alt_failure = 'C:/Users/deepz/Downloads/ulog/processed/processed/carbonZ_2018-09-11-11-56-30_engine_failure/carbonZ_2018-09-11-11-56-30_engine_failure-mavros-global_position-rel_alt.csv'
    vel_failure = 'C:/Users/deepz/Downloads/ulog/processed/processed/carbonZ_2018-09-11-11-56-30_engine_failure/carbonZ_2018-09-11-11-56-30_engine_failure-mavros-local_position-velocity.csv'

    normal_df = load_and_align(alt_normal, vel_normal)
    failure_df = load_and_align(alt_failure, vel_failure)

    sca, pca = fit_pca(normal_df, 0.95)
    anomaly_scores = compute_anomaly_score(failure_df, sca, pca)

    threshold = anomaly_scores.mean() + 3 * anomaly_scores.std()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    # Top: original altitude
    ax1.plot(failure_df['time_sec'], failure_df['altitude'], color='blue')
    ax1.set_ylabel('Altitude (m)')
    ax1.set_title('Altitude - Engine Failure Flight')
    ax1.grid(True)

    # Bottom: anomaly score
    ax2.plot(failure_df['time_sec'], anomaly_scores, color='orange')
    ax2.axhline(threshold, color='red', linestyle='--', label='Threshold')
    for time, score in zip(failure_df['time_sec'], anomaly_scores):
        if score > threshold:
            ax2.axvline(time, color='r', alpha=0.15)
    ax2.set_ylabel('Anomaly Score')
    ax2.set_xlabel('Time (seconds)')
    ax2.set_title('PCA Anomaly Score')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('figures/altitude_comparison.png', dpi=150)
    plt.show()

    