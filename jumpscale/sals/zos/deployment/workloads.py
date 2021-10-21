from jumpscale.core.base import Base, fields, StoredFactory
from jumpscale.core.base.fields import List

from jumpscale.sals.zos.workload import Workload, WorkloadTypes
from jumpscale.sals.zos.workload.znet import Znet, Peer
from jumpscale.sals.zos.workload.zmount import Zmount
from jumpscale.sals.zos.workload.zmachine import Zmachine, ZmachineNetwork, ZNetworkInterface, Mount, ComputeCapacity
from jumpscale.sals.zos.workload.zdb import Zdb
from jumpscale.sals.zos.workload.ipv4 import Ipv4


class Workloads(list):
    def add_zmachine(
        self,
        name,
        version,
        metadata,
        description,
        mount_name,
        mountpoint,
        network_name,
        network_ip,
        planetary,
        public_ip_name,
        cpu,
        memory,
        flist_url,
        size,
        entrypoint,
        env: dict,
    ):
        mount = Mount(name=mount_name, mountpoint=mountpoint)

        znetwork_interface = ZNetworkInterface(network=network_name, ip=network_ip)

        zmachine_network = ZmachineNetwork(
            planetary=planetary, interfaces=[znetwork_interface], public_ip=public_ip_name
        )

        compute_capacity = ComputeCapacity(cpu=cpu, memory=memory)

        zmachine = Zmachine(
            flist=flist_url,
            network=zmachine_network,
            size=size,
            mounts=[mount],
            entrypoint=entrypoint,
            compute_capacity=compute_capacity,
            env=env,
        )

        zmachine_workload = Workload(
            version=version,
            name=name,
            type=WorkloadTypes.zmachine,
            data=zmachine,
            metadata=metadata,
            description=description,
        )
        self.append(zmachine_workload)

        return zmachine_workload

    def add_zmount(
        self, name, version, metadata, description, size,
    ):
        zmount = Zmount(size=size)

        zmount_workload = Workload(
            version=version,
            name=name,
            type=WorkloadTypes.zmount,
            data=zmount,
            metadata=metadata,
            description=description,
        )
        self.append(zmount_workload)

        return zmount_workload

    def add_network(
        self,
        name,
        version,
        metadata,
        description,
        znet_subnet,
        ip_range,
        wireguard_private_key,
        wireguard_listen_port,
        peers: list,
    ):
        # peer = Peer(
        #     subnet="10.240.2.0/24",
        #     wireguard_public_key="cEzVprB7IdpLaWZqYOsCndGJ5MBgv1q1lTFG1B2Czkc=",
        #     allowed_ips=["10.240.2.0/24", "100.64.240.2/32"],
        # )

        znet = Znet(
            subnet=znet_subnet,
            ip_range=ip_range,
            wireguard_private_key=wireguard_private_key,
            wireguard_listen_port=wireguard_listen_port,
            peers=peers,
        )

        znet_workload = Workload(
            version=version,
            name=name,
            type=WorkloadTypes.network,
            data=znet,
            metadata=metadata,
            description=description,
        )
        self.append(znet_workload)
        return znet_workload

    def add_zdb(self, name, version, metadata, description, namespace, size, mode, password, disk_type, public):
        zdb = Zdb(namespace=namespace, size=size, mode=mode, password=password, disk_type=disk_type, public=public)

        zdb_workload = Workload(
            version=version, name=name, type=WorkloadTypes.zdb, data=zdb, metadata=metadata, description=description,
        )
        self.append(zdb_workload)
        return zdb_workload

    def add_ipv4(self, name, version, metadata, description):
        zpub_ip = Ipv4()

        zpub_ip_workload = Workload(
            version=version,
            name=name,
            type=WorkloadTypes.ipv4,
            data=zpub_ip,
            description=description,
            metadata=metadata,
        )
        self.append(zpub_ip_workload)
        return zpub_ip_workload
