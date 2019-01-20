from Pirates_Conference import pirates_conference
from Up_Down_Trans import Up_Down_Transf
from Pirates import pirates


def Flying_Dutchman():
    org_raw_data = pirates()

    big_table = Up_Down_Transf(org_raw_data)

    big_df = pirates_conference(big_table)

    return big_df