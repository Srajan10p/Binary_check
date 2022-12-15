def get_bmc_ip_silicon(cfg_opts):
    """Importing BMC ip from system config file: silicon bmc tag"""
    try:
        bmc_ip = cfg_opts.find("suts/sut/silicon/bmc/ip").text
    except Exception:
        bmc_ip = cfg_opts.find("suts/sut/silicon/bmc/ipv4").text
    return bmc_ip


def get_bmc_ip_redfish(cfg_opts):
    """Importing BMC ip from system config file: redfish tag"""
    try:
        bmc_ip = cfg_opts.find("suts/sut/providers/flash/driver/redfish/ip").text
    except Exception:
        bmc_ip = cfg_opts.find("suts/sut/providers/flash/driver/redfish/ipv4").text
    return bmc_ip