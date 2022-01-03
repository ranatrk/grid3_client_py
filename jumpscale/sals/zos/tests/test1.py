import asyncio

from jumpscale.sals.zos.workload.network import Znet, Peer
from jumpscale.sals.zos.workload.zmount import Zmount
from jumpscale.sals.zos.workload.zmachine import Zmachine, ZmachineNetwork, ZNetworkInterface, Mount, ComputeCapacity
from jumpscale.sals.zos.workload.ipv4 import Ipv4

# from jumpscale.sals.zos.workload.computecapacity import ComputeCapacity
from jumpscale.sals.zos.workload import Workload, WorkloadTypes
from jumpscale.sals.zos.deployment import Deployment, SignatureRequirement, SignatureRequest
from jumpscale.loader import j

RMB_PROXY_URL = "https://gridproxy.dev.grid.tf"


def test():
    twin_id = 54
    mnemonic = "magnet wage miracle spirit oval sport input boat glide basic grass spike"
    url = "wss://tfchain.dev.grid.tf/ws"
    node_id = 7
    node_twin_id = 12
    ssh_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCt1LYcIga3sgbip5ejiC6R7CCa34omOwUilR66ZEvUh/u4RpbZ9VjRryVHVDyYcd/qbUzpWMzqzFlfFmtVhPQ0yoGhxiv/owFwStqddKO2iNI7T3U2ytYLJqtPm0JFLB5n07XLyFRplq0W2/TjNrYl51DedDQqBJDq34lz6vTkECNmMKg9Ld0HpxnpHBLH0PsXMY+JMZ8keH9hLBK61Mx9cnNxcLV9N6oA6xRCtwqOdLAH08MMaItYcJ0UF/PDs1PusJvWkvsH5/olgayeAReI6JFGv/x4Eqq5vRJRQjkj9m+Q275gzf9Y/7M/VX7KOH7P9HmDbxwRtOq1F0bRutKF"
    contract_id = 18  # used only in case of updating deployment.
    rmb_proxy_client = j.clients.rmb_http.get("test1", proxy_url=RMB_PROXY_URL, twin_id=twin_id)

    # Create zmount workload
    zmount = Zmount(size=1024 * 1024 * 1024 * 10)

    zmount_workload = Workload(
        version=0, name="zmountiaia", type=WorkloadTypes.Zmount, data=zmount, metadata="zm", description="zm test"
    )

    # Create zmount workload
    zmount1 = Zmount(size=1024 * 1024 * 1024 * 10)

    zmount_workload1 = Workload(
        version=0, name="zmountiaia1", type=WorkloadTypes.Zmount, data=zmount, metadata="zm1", description="zm test1"
    )

    # Create znet workload
    peer = Peer(
        subnet="10.240.2.0/24",
        wireguard_public_key="cEzVprB7IdpLaWZqYOsCndGJ5MBgv1q1lTFG1B2Czkc=",
        allowed_ips=["10.240.2.0/24", "100.64.240.2/32"],
        endpoint="",
    )

    znet = Znet(
        subnet="10.240.1.0/24",
        ip_range="10.240.0.0/16",
        wireguard_private_key="SDtQFBHzYTu/c7dt/X1VDZeGmXmE7TD6nQC5tp4wv38=",
        wireguard_listen_port=6835,
        peers=[peer],
    )

    znet_workload = Workload(
        version=0, name="testznetwork1", type=WorkloadTypes.Znet, data=znet, metadata="zn", description="zn test"
    )

    # create a public ip
    zpub_ip = Ipv4()

    # create public ip workload
    zpub_ip_workload = Workload(
        version=0, name="zpub", type=WorkloadTypes.Ipv4, data=zpub_ip, description="my zpub ip", metadata="zpub ip",
    )

    # create zmachine workload
    mount = Mount(name="zmountiaia", mountpoint="/mydisk")

    znetwork_interface = ZNetworkInterface(network="testznetwork1", ip="10.240.1.5")

    zmachine_network = ZmachineNetwork(planetary=True, interfaces=[znetwork_interface], public_ip="zpub")

    compute_capacity = ComputeCapacity(cpu=1, memory=1024 * 1024 * 1024 * 2)

    zmachine = Zmachine(
        flist="https://hub.grid.tf/ahmed_hanafy_1/ahmedhanafy725-k3s-latest.flist",
        network=zmachine_network,
        size=256 * 1024 * 1024,
        mounts=[mount],
        entrypoint="/sbin/zinit init",
        compute_capacity=compute_capacity,
        env={
            "SSH_KEY": ssh_key,
            "K3S_TOKEN": "hamadaellol",
            "K3S_DATA_DIR": "/mydisk",
            "K3S_FLANNEL_IFACE": "eth0",
            "K3S_NODE_NAME": "hamada",
            "K3S_URL": "",
        },
    )

    zmachine_workload = Workload(
        version=0,
        name="testzmachine",
        type=WorkloadTypes.Zmachine,
        data=zmachine,
        metadata="zmachine",
        description="zmachine test",
    )

    # create zmachine workload
    mount1 = Mount(name="zmountiaia1", mountpoint="/mydisk",)

    znetwork_interface1 = ZNetworkInterface(network="testznetwork1", ip="10.240.1.6",)

    zmachine_network1 = ZmachineNetwork(planetary=True, interfaces=[znetwork_interface1],)

    compute_capacity1 = ComputeCapacity(cpu=1, memory=1024 * 1024 * 1024 * 2)

    zmachine1 = Zmachine(
        flist="https://hub.grid.tf/ahmed_hanafy_1/ahmedhanafy725-k3s-latest.flist",
        network=zmachine_network1,
        size=256 * 1024 * 1024,
        mounts=[mount1],
        entrypoint="/sbin/zinit init",
        compute_capacity=compute_capacity1,
        env={
            "SSH_KEY": ssh_key,
            "K3S_TOKEN": "hamadaellol",
            "K3S_DATA_DIR": "/mydisk",
            "K3S_FLANNEL_IFACE": "eth0",
            "K3S_NODE_NAME": "worker",
            "K3S_URL": "https://10.240.1.5:6443",
        },
    )

    zmachine_workload1 = Workload(
        version=0,
        name="testzmachine1",
        type=WorkloadTypes.Zmachine,
        data=zmachine1,
        metadata="zmachine1",
        description="zmachine test1",
    )

    # Create deployment
    signature_request = SignatureRequest(twin_id=twin_id, weight=1,)

    signature_requirement = SignatureRequirement(weight_required=1, requests=[signature_request])

    deployment = Deployment(
        version=0,
        twin_id=twin_id,
        expiration=1626394558,
        metadata="zm dep",
        description="zm test",
        workloads=[
            zmount_workload,
            zmount_workload1,
            znet_workload,
            # zpub_ip_workload,
            zmachine_workload,
            zmachine_workload1,
        ],
        signature_requirement=signature_requirement,
    )

    print(deployment.challenge_hash())
    print(deployment.challenge())
    deployment.sign(twin_id, mnemonic)

    tf_client = j.clients.tfgrid.get("test", url, mnemonic)

    def deploy():
        contract_created = tf_client.contract.create_node_contract(
            nodeID=node_id, data="", hash=deployment.challenge_hash(), numberOfPublicIPs=0
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
        j.logger.info(f"Deployment result from rmb-proxy read : {read_result}")

    deploy()
    # update()


print(test())
