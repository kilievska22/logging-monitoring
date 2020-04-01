#prometheus
Prometheus is a monitoring solution that gathers time-series based numerical data.
#collect metrics exposed by this app with prometheus
1.Copy one of the following configuration files and save it to /tmp/prometheus.yml (Linux or Mac) or C:\tmp\prometheus.yml (Windows).
This is a  Prometheus configuration file for Windows, except for the addition of the Docker job definition at the bottom of the file.
Docker Desktop for Mac and Docker Desktop for Linux need a slightly different configuration.
# my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
      monitor: 'codelab-monitor'

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first.rules"
  # - "second.rules"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ['docker.for.win.localhost:9090']

  - job_name: 'docker_fast_api'
         # metrics_path defaults to '/metrics'
         # scheme defaults to 'http'.

    static_configs:
      - targets: ['docker.for.win.localhost:80']



2.run this from windows powershell
PS C:\> docker service create --replicas 1 --name my-prometheus
    --mount type=bind,source=C:/tmp/prometheus.yml,destination=/etc/prometheus/prometheus.yml
    --publish published=9090,target=9090,protocol=tcp
    prom/prometheus


#start the app container
Go to the project directory (in where your docker-compose.yml is, containing your app directory) and type docker-compose up.
Now you can make api calls in your Docker container's URL, for example: http://192.168.99.100:80/update/count or http://127.0.0.1:80/update/count.
Graphanna is running on port 3000 and Prometheus on port 9090.



