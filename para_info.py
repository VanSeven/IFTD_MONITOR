# -*- coding: utf-8 -*-

# Name: iftd_monitor
# Description: IFTD实时监控软件
# Author: Wang Xueliang
# Date: 2019/6/22

PARA_LIST = ['Time', 'PF_UPST_L', 'PF_DNST_L', 'TF_UPST_L', 'TF_DNST_L', 'QF_UPS_L', 'QF_DNS_L',
             'PT_15R1A_L', 'PT_15R1B_L', 'PT_15R1C_L', 'PT_15R1D_L',
             'PT_15R1E_L', 'PT_15R1F_L', 'PT_15R1G_L', 'PT_15R1H_L',
             'PT_15R2A_L', 'PT_15R2B_L', 'PT_15R2C_L', 'PT_15R2D_L',
             'PT_15R2E_L', 'PT_15R2F_L', 'PT_15R2G_L', 'PT_15R2H_L',
             'PT_15R3A_L', 'PT_15R3B_L', 'PT_15R3C_L', 'PT_15R3D_L',
             'PT_15R3E_L', 'PT_15R3F_L', 'PT_15R3G_L', 'PT_15R3H_L',
             'PT_15R4A_L', 'PT_15R4B_L', 'PT_15R4C_L', 'PT_15R4D_L',
             'PT_15R4E_L', 'PT_15R4F_L', 'PT_15R4G_L', 'PT_15R4H_L',
             'PT_15R5A_L', 'PT_15R5B_L', 'PT_15R5C_L', 'PT_15R5D_L',
             'PT_15R5E_L', 'PT_15R5F_L', 'PT_15R5G_L', 'PT_15R5H_L',
             'PT_15R6A_L', 'PT_15R6B_L', 'PT_15R6C_L', 'PT_15R6D_L',
             'PT_15R6E_L', 'PT_15R6F_L', 'PT_15R6G_L', 'PT_15R6H_L',
             'PT_15R7A_L', 'PT_15R7B_L', 'PT_15R7C_L', 'PT_15R7D_L',
             'PT_15R7E_L', 'PT_15R7F_L', 'PT_15R7G_L', 'PT_15R7H_L',
             'PT_15R8A_L', 'PT_15R8B_L', 'PT_15R8C_L', 'PT_15R8D_L',
             'PT_15R8E_L', 'PT_15R8F_L', 'PT_15R8G_L', 'PT_15R8H_L',
             ]

TIME_RANGE_PARA_LEFT = ['PF_UPST_L', 'TF_UPST_L', 'QF_UPS_L', 'PF_DNST_L', 'TF_DNST_L', 'QF_DNS_L']
TIME_RANGE_PARA_RIGHT = ['PF_UPST_R', 'TF_UPST_R', 'QF_UPS_R', 'PF_DNST_R', 'TF_DNST_R', 'QF_DNS_R']

TIME_PARA_LEFT = {'PT_15R1_L': ['PT_15R1A_L', 'PT_15R1B_L', 'PT_15R1C_L', 'PT_15R1D_L',
                                'PT_15R1E_L', 'PT_15R1F_L', 'PT_15R1G_L', 'PT_15R1H_L'],
                  'PT_15R2_L': ['PT_15R2A_L', 'PT_15R2B_L', 'PT_15R2C_L', 'PT_15R2D_L',
                                'PT_15R2E_L', 'PT_15R2F_L', 'PT_15R2G_L', 'PT_15R2H_L'],
                  'PT_15R3_L': ['PT_15R3A_L', 'PT_15R3B_L', 'PT_15R3C_L', 'PT_15R3D_L',
                                'PT_15R3E_L', 'PT_15R3F_L', 'PT_15R3G_L', 'PT_15R3H_L'],
                  'PT_15R4_L': ['PT_15R4A_L', 'PT_15R4B_L', 'PT_15R4C_L', 'PT_15R4D_L',
                                'PT_15R4E_L', 'PT_15R4F_L', 'PT_15R4G_L', 'PT_15R4H_L'],
                  'PT_15R5_L': ['PT_15R5A_L', 'PT_15R5B_L', 'PT_15R5C_L', 'PT_15R5D_L',
                                'PT_15R5E_L', 'PT_15R5F_L', 'PT_15R5G_L', 'PT_15R5H_L'],
                  'PT_15R6_L': ['PT_15R6A_L', 'PT_15R6B_L', 'PT_15R6C_L', 'PT_15R6D_L',
                                'PT_15R6E_L', 'PT_15R6F_L', 'PT_15R6G_L', 'PT_15R6H_L'],
                  'PT_15R7_L': ['PT_15R7A_L', 'PT_15R7B_L', 'PT_15R7C_L', 'PT_15R7D_L',
                                'PT_15R7E_L', 'PT_15R7F_L', 'PT_15R7G_L', 'PT_15R7H_L'],
                  'PT_15R8_L': ['PT_15R8A_L', 'PT_15R8B_L', 'PT_15R8C_L', 'PT_15R8D_L',
                                'PT_15R8E_L', 'PT_15R8F_L', 'PT_15R8G_L', 'PT_15R8H_L']
                  }

TIME_PARA_RIGHT = {'PT_15R1_R': ['PT_15R1A_R', 'PT_15R1B_R', 'PT_15R1C_R', 'PT_15R1D_R',
                                 'PT_15R1E_R', 'PT_15R1F_R', 'PT_15R1G_R', 'PT_15R1H_R'],
                   'PT_15R2_R': ['PT_15R2A_R', 'PT_15R2B_R', 'PT_15R2C_R', 'PT_15R2D_R',
                                 'PT_15R2E_R', 'PT_15R2F_R', 'PT_15R2G_R', 'PT_15R2H_R'],
                   'PT_15R3_R': ['PT_15R3A_R', 'PT_15R3B_R', 'PT_15R3C_R', 'PT_15R3D_R',
                                 'PT_15R3E_R', 'PT_15R3F_R', 'PT_15R3G_R', 'PT_15R3H_R'],
                   'PT_15R4_R': ['PT_15R4A_R', 'PT_15R4B_R', 'PT_15R4C_R', 'PT_15R4D_R',
                                 'PT_15R4E_R', 'PT_15R4F_R', 'PT_15R4G_R', 'PT_15R4H_R'],
                   'PT_15R5_R': ['PT_15R5A_R', 'PT_15R5B_R', 'PT_15R5C_R', 'PT_15R5D_R',
                                 'PT_15R5E_R', 'PT_15R5F_R', 'PT_15R5G_R', 'PT_15R5H_R'],
                   'PT_15R6_R': ['PT_15R6A_R', 'PT_15R6B_R', 'PT_15R6C_R', 'PT_15R6D_R',
                                 'PT_15R6E_R', 'PT_15R6F_R', 'PT_15R6G_R', 'PT_15R6H_R'],
                   'PT_15R7_R': ['PT_15R7A_R', 'PT_15R7B_R', 'PT_15R7C_R', 'PT_15R7D_R',
                                 'PT_15R7E_R', 'PT_15R7F_R', 'PT_15R7G_R', 'PT_15R7H_R'],
                   'PT_15R8_R': ['PT_15R8A_R', 'PT_15R8B_R', 'PT_15R8C_R', 'PT_15R8D_R',
                                 'PT_15R8E_R', 'PT_15R8F_R', 'PT_15R8G_R', 'PT_15R8H_R']
                   }

