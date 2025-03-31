# Grafana to Atlassian Statuspage Webhook

This application is a **Flask-based webhook handler** designed to integrate **Grafana alerts** with **Atlassian Statuspage**. It listens for incoming webhook requests from Grafana, processes the alert data, and updates the status of components on Atlassian Statuspage based on the alert's status.

## Features

- **Webhook Endpoint**: Exposes a `/webhook` endpoint to receive `POST` and `PUT` requests from Grafana.
- **Status Mapping**: Maps Grafana alert statuses to Statuspage component statuses:
  - `firing` → `major_outage`
  - `resolved` → `operational`
  - `no_data` → `under_maintenance`
  - `paused` → `under_maintenance`
- **Dynamic Payload Resending**: Constructs and sends a `PUT` request to the Atlassian Statuspage API to update the status of the specified component.
- **Environment Variables**: Configurable via environment variables for flexibility and security.
- **Logging**: Logs key information for debugging and monitoring

## Public Docker Registry

The Docker image for this application is available on Docker Hub:

[https://hub.docker.com/r/iolesyk/grafana-atlassian-statuspage-webhook](https://hub.docker.com/r/iolesyk/grafana-atlassian-statuspage-webhook)

You can pull the image using:
```
docker pull iolesyk/grafana-atlassian-statuspage-webhook:latest
```

## Example docker build

```
docker buildx build --platform linux/amd64,linux/arm64 -t grafana-atlassian-statuspage-webhook .
```

## Example docker run

```
docker run -p 6000:6000 \
--env FLASK_RUN_PORT=6000 \
--env STATUSPAGE_API_URL=https://api.statuspage.io \
--env STATUSPAGE_API_BEARER_TOKEN=<TOKEN>\
grafana-atlassian-statuspage-webhook
```

## Example Grafana configuration

Alert rule - annotations
```
{"page": "STATUS_PAGE_ID","component": "STATUS_PAGE_COMPONENT_ID","instance":"test.com"}
```
