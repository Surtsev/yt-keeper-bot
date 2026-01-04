# Auto-generated using compose2nix v0.3.1.
{ pkgs, lib, ... }:

{
  # Runtime
  virtualisation.docker = {
    enable = true;
    autoPrune.enable = true;
  };
  virtualisation.oci-containers.backend = "docker";

  # Containers
  virtualisation.oci-containers.containers."ytkeeper_api" = {
    image = "ytkeeper_api";
    environment = {
      "DB_NAME" = "ytkeeper_db";
      "DB_PASSWORD" = "192837";
      "DB_URL" = "postgresql+asyncpg://ytkeeper:192837@db:5432/ytkeeper_db";
      "DB_USER" = "ytkeeper";
      "URL" = "http://nginx:80";
    };
    dependsOn = [
      "ytkeeper_db"
    ];
    log-driver = "journald";
    extraOptions = [
      "--health-cmd=[\"curl\", \"-f\", \"http://localhost:8000/docs\"]"
      "--health-interval=10s"
      "--health-retries=3"
      "--health-timeout=5s"
      "--network-alias=api"
      "--network=ytkeeper_ytkeeper_network"
    ];
  };
  systemd.services."docker-ytkeeper_api" = {
    serviceConfig = {
      Restart = lib.mkOverride 90 "always";
      RestartMaxDelaySec = lib.mkOverride 90 "1m";
      RestartSec = lib.mkOverride 90 "100ms";
      RestartSteps = lib.mkOverride 90 9;
    };
    after = [
      "docker-network-ytkeeper_ytkeeper_network.service"
    ];
    requires = [
      "docker-network-ytkeeper_ytkeeper_network.service"
    ];
    partOf = [
      "docker-compose-ytkeeper-root.target"
    ];
    wantedBy = [
      "docker-compose-ytkeeper-root.target"
    ];
  };
  virtualisation.oci-containers.containers."ytkeeper_db" = {
    image = "postgres:16-alpine";
    environment = {
      "POSTGRES_DB" = "ytkeeper_db";
      "POSTGRES_INITDB_ARGS" = "-c shared_buffers=256MB -c max_connections=200";
      "POSTGRES_PASSWORD" = "192837";
      "POSTGRES_USER" = "ytkeeper";
    };
    volumes = [
      "ytkeeper_postgres_data:/var/lib/postgresql/data:rw"
    ];
    log-driver = "journald";
    extraOptions = [
      "--health-cmd=pg_isready -U ytkeeper -d ytkeeper_db"
      "--health-interval=10s"
      "--health-retries=5"
      "--health-start-period=30s"
      "--health-timeout=5s"
      "--network-alias=db"
      "--network=ytkeeper_ytkeeper_network"
    ];
  };
  systemd.services."docker-ytkeeper_db" = {
    serviceConfig = {
      Restart = lib.mkOverride 90 "always";
      RestartMaxDelaySec = lib.mkOverride 90 "1m";
      RestartSec = lib.mkOverride 90 "100ms";
      RestartSteps = lib.mkOverride 90 9;
    };
    after = [
      "docker-network-ytkeeper_ytkeeper_network.service"
      "docker-volume-ytkeeper_postgres_data.service"
    ];
    requires = [
      "docker-network-ytkeeper_ytkeeper_network.service"
      "docker-volume-ytkeeper_postgres_data.service"
    ];
    partOf = [
      "docker-compose-ytkeeper-root.target"
    ];
    wantedBy = [
      "docker-compose-ytkeeper-root.target"
    ];
  };
  virtualisation.oci-containers.containers."ytkeeper_nginx" = {
    image = "nginx:alpine";
    volumes = [
      "/home/surtsev/Projects/yt-keeper-bot/nginx.conf:/etc/nginx/nginx.conf:ro"
    ];
    ports = [
      "3000:80/tcp"
    ];
    dependsOn = [
      "ytkeeper_api"
    ];
    log-driver = "journald";
    extraOptions = [
      "--network-alias=nginx"
      "--network=ytkeeper_ytkeeper_network"
    ];
  };
  systemd.services."docker-ytkeeper_nginx" = {
    serviceConfig = {
      Restart = lib.mkOverride 90 "always";
      RestartMaxDelaySec = lib.mkOverride 90 "1m";
      RestartSec = lib.mkOverride 90 "100ms";
      RestartSteps = lib.mkOverride 90 9;
    };
    after = [
      "docker-network-ytkeeper_ytkeeper_network.service"
    ];
    requires = [
      "docker-network-ytkeeper_ytkeeper_network.service"
    ];
    partOf = [
      "docker-compose-ytkeeper-root.target"
    ];
    wantedBy = [
      "docker-compose-ytkeeper-root.target"
    ];
  };

  # Networks
  systemd.services."docker-network-ytkeeper_ytkeeper_network" = {
    path = [ pkgs.docker ];
    serviceConfig = {
      Type = "oneshot";
      RemainAfterExit = true;
      ExecStop = "docker network rm -f ytkeeper_ytkeeper_network";
    };
    script = ''
      docker network inspect ytkeeper_ytkeeper_network || docker network create ytkeeper_ytkeeper_network --driver=bridge
    '';
    partOf = [ "docker-compose-ytkeeper-root.target" ];
    wantedBy = [ "docker-compose-ytkeeper-root.target" ];
  };

  # Volumes
  systemd.services."docker-volume-ytkeeper_postgres_data" = {
    path = [ pkgs.docker ];
    serviceConfig = {
      Type = "oneshot";
      RemainAfterExit = true;
    };
    script = ''
      docker volume inspect ytkeeper_postgres_data || docker volume create ytkeeper_postgres_data --driver=local
    '';
    partOf = [ "docker-compose-ytkeeper-root.target" ];
    wantedBy = [ "docker-compose-ytkeeper-root.target" ];
  };

  # Builds
  systemd.services."docker-build-ytkeeper_api" = {
    path = [ pkgs.docker pkgs.git ];
    serviceConfig = {
      Type = "oneshot";
      TimeoutSec = 300;
    };
    script = ''
      cd /home/surtsev/Projects/yt-keeper-bot
      docker build -t compose2nix/ytkeeper_api -f ./Dockerfile .
    '';
  };

  # Root service
  # When started, this will automatically create all resources and start
  # the containers. When stopped, this will teardown all resources.
  systemd.targets."docker-compose-ytkeeper-root" = {
    unitConfig = {
      Description = "Root target generated by compose2nix.";
    };
    wantedBy = [ "multi-user.target" ];
  };
}
