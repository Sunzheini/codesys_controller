# A collection of all test case names and time limits

TEST_CASES = {
            '00': ("T00_Init_Drive", 2),
            '01': ("T01_MC_Power_Festo", 2),
            '02': ("T02_MC_Reset_Festo", 2),
            '03': ("T03_MC_Home_Festo", 25),
            '04': ("T04_MC_MoveAbsolute_Festo", 15),
            '05': ("T05_MC_MoveRelative_Festo", 15),
            '06': ("T06_MC_MoveAdditive_Festo", 15),
            '07': ("T07_MC_MoveVelocity_Festo", 15),
            '08': ("T08_MC_TorqueControl_Festo", 15),
            '09': ("T09_MC_RecordTable_Festo", 15),
            '10': ("T10_MC_Halt_Festo", 15),
            '11': ("T11_MC_Stop_Festo", 15),
            '12': ("T12_Buffered_Festo", 15),
            '13': ("T13_Aborting_Festo", 15),
            '14': ("T14_MC_ReadWriteParameter_Festo", 15),
            '15': ("T15_MC_ReadWriteStringParameter_Festo", 15),
            '16': ("T16_MC_ReadActualPositionVelocityTorque_Festo", 15),
            '17': ("T17_MC_ReadStatus_Festo", 15),
            '18': ("T18_MC_ReadAxisError_Festo", 15),
            '19': ("T19_MC_ReadAxisInfo_Festo", 15),
            '20': ("T20_MC_Methodenaufruf", 4),
            '21': ("T21_MC_Jog_Festo", 15),
            '22': ("T22_MC_DeviceService_Festo", 15),
        }
