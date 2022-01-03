import asyncio

from jumpscale.sals.zos.deployment import Deployment, SignatureRequirement, SignatureRequest
from jumpscale.loader import j

RMB_PROXY_URL = "https://gridproxy.dev.grid.tf"


def test():
    twin_id = 23
    mnemonic = "magnet wage miracle spirit oval sport input boat glide basic grass spike"
    url = "wss://tfchain.dev.grid.tf/ws"
    node_id = 7
    node_twin_id = 10
    ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCt1LYcIga3sgbip5ejiC6R7CCa34omOwUilR66ZEvUh/u4RpbZ9VjRryVHVDyYcd/qbUzpWMzqzFlfFmtVhPQ0yoGhxiv/owFwStqddKO2iNI7T3U2ytYLJqtPm0JFLB5n07XLyFRplq0W2/TjNrYl51DedDQqBJDq34lz6vTkECNmMKg9Ld0HpxnpHBLH0PsXMY+JMZ8keH9hLBK61Mx9cnNxcLV9N6oA6xRCtwqOdLAH08MMaItYcJ0UF/PDs1PusJvWkvsH5/olgayeAReI6JFGv/x4Eqq5vRJRQjkj9m+Q275gzf9Y/7M/VX7KOH7P9HmDbxwRtOq1F0bRutKF"
    contract_id = 189  # used only in case of updating deployment.

    rmb_proxy_client = j.clients.rmb_http.get("test1", proxy_url=RMB_PROXY_URL, twin_id=twin_id)

    # Create deployment
    signature_request = SignatureRequest(twin_id=twin_id, weight=1,)

    signature_requirement = SignatureRequirement(weight_required=1, requests=[signature_request])

    deployment = Deployment(
        version=0,
        twin_id=twin_id,
        expiration=1626394539,
        metadata="zm dep",
        description="zm test",
        signature_requirement=signature_requirement,
    )

    # workloads = [zmount_workload, zmount_workload1, znet_workload, zpub_ip_workload, zmachine_workload, zmachine_workload1];

    ## Create zmount workload
    deployment.workloads.add_zmount(
        name="zmountiaia", version=0, metadata="zm", description="zm test", size=1024 * 1024 * 1024 * 10
    )
    # Create zmount workload
    deployment.workloads.add_zmount(
        name="zmountiaia1", version=0, metadata="zm1", description="zm test1", size=1024 * 1024 * 1024 * 10
    )

    ## Create znet workload
    peer = {
        "subnet": "10.240.2.0/24",
        "wireguard_public_key": "cEzVprB7IdpLaWZqYOsCndGJ5MBgv1q1lTFG1B2Czkc=",
        "allowed_ips": ["10.240.2.0/24", "100.64.240.2/32"],
        "endpoint": "",
    }
    deployment.workloads.add_network(
        name="testznetwork1",
        version=0,
        metadata="zn",
        description="zn test",
        znet_subnet="10.240.1.0/24",
        ip_range="10.240.0.0/16",
        wireguard_private_key="SDtQFBHzYTu/c7dt/X1VDZeGmXmE7TD6nQC5tp4wv38=",
        wireguard_listen_port=6835,
        peers=[peer],
    )

    ## create a public ip
    deployment.workloads.add_ipv4(
        name="zpub", version=0, description="my zpub ip", metadata="zpub ip",
    )

    ## create zmachine workload
    deployment.workloads.add_zmachine(
        name="testzmachine",
        version=0,
        metadata="zmachine",
        description="zmachine test",
        mount_name="zmountiaia",
        mountpoint="/mydisk",
        network_name="testznetwork1",
        network_ip="10.240.1.5",
        planetary=True,
        public_ip_name="zpub",
        cpu=1,
        memory=1024 * 1024 * 1024 * 2,
        flist_url="https://hub.grid.tf/ahmed_hanafy_1/ahmedhanafy725-k3s-latest.flist",
        size=256 * 1024 * 1024,
        entrypoint="/sbin/zinit init",
        env={
            "SSH_KEY": ssh_key,
            "K3S_TOKEN": "hamadaellol",
            "K3S_DATA_DIR": "/mydisk",
            "K3S_FLANNEL_IFACE": "eth0",
            "K3S_NODE_NAME": "hamada",
            "K3S_URL": "",
        },
    )

    ## create zmachine workload
    deployment.workloads.add_zmachine(
        name="testzmachine1",
        version=0,
        metadata="zmachine1",
        description="zmachine test1",
        mount_name="zmountiaia1",
        mountpoint="/mydisk",
        network_name="testznetwork1",
        network_ip="10.240.1.6",
        planetary=True,
        public_ip_name="",
        cpu=1,
        memory=1024 * 1024 * 1024 * 2,
        flist_url="https://hub.grid.tf/ahmed_hanafy_1/ahmedhanafy725-k3s-latest.flist",
        size=256 * 1024 * 1024,
        entrypoint="/sbin/zinit init",
        env={
            "SSH_KEY": ssh_key,
            "K3S_TOKEN": "hamadaellol",
            "K3S_DATA_DIR": "/mydisk",
            "K3S_FLANNEL_IFACE": "eth0",
            "K3S_NODE_NAME": "worker",
            "K3S_URL": "https://10.240.1.5:6443",
        },
    )
    print(deployment.challenge_hash())
    print(deployment.challenge())
    deployment.sign(twin_id, mnemonic)

    tf_client = j.clients.tfgrid.get("test", url, mnemonic)

    def deploy():
        contract_created = tf_client.contract.create_node_contract(
            nodeID=node_id, data="", hash=deployment.challenge_hash(), numberOfPublicIPs=1
        )
        if contract_created:
            data = tf_client.contract.get(node_id=node_id, data_hash=deployment.challenge_hash())
        else:
            raise RuntimeError("Contract creation failed")
        print(data)
        deployment.contract_id = data["contract_id"]

        payload = j.data.serializers.json.dumps(deployment.to_dict())
        print("payload>>>>>>>>>>>>>>>>>>", payload)

        message = rmb_proxy_client.prepare(
            command="zos.deployment.deploy", destination=[node_twin_id], expiration=20, retry=2
        )

        send_result = rmb_proxy_client.send(message, payload)
        read_result = rmb_proxy_client.read(send_result)
        j.logger.info(f"Deployment result from rmb-proxy read : {read_result}")

    def update():
        tf_client.contract.update_node_contract(contract_id, "", deployment.challenge_hash())
        deployment.contract_id = contract_id
        payload = j.data.serializers.json.dumps(deployment.to_dict())
        print("payload>>>>>>>>>>>>>>>>>>", payload)

        message = rmb_proxy_client.prepare(
            command="zos.deployment.update", destination=[node_twin_id], expiration=20, retry=2
        )

        send_result = rmb_proxy_client.send(message, payload)
        read_result = rmb_proxy_client.read(send_result)
        j.logger.info(f"Deployment update result from rmb-proxy read : {read_result}")

    deploy()


print(test())
