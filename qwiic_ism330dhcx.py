#-------------------------------------------------------------------------------
# qwiic_ism330dhcx.py
#
# Python library for the SparkFun Qwiic ISM330DHCX, available here:
# https://www.sparkfun.com/products/19764
#-------------------------------------------------------------------------------
# Written by SparkFun Electronics, December 2024
#
# This python library supports the SparkFun Electroncis Qwiic ecosystem
#
# More information on Qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#===============================================================================
# Copyright (c) 2023 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#===============================================================================

"""
qwiic_ism330dhcx
============
Python module for the [SparkFun Qwiic ISM330DHCX](https://www.sparkfun.com/products/19764)
This is a port of the existing [Arduino Library](https://github.com/sparkfun/SparkFun_6DoF_ISM330DHCX_Arduino_Library)
This package can be used with the overall [SparkFun Qwiic Python Package](https://github.com/sparkfun/Qwiic_Py)
New to Qwiic? Take a look at the entire [SparkFun Qwiic ecosystem](https://www.sparkfun.com/qwiic).
"""

# The Qwiic_I2C_Py platform driver is designed to work on almost any Python
# platform, check it out here: https://github.com/sparkfun/Qwiic_I2C_Py
import qwiic_i2c

# Define the device name and I2C addresses. These are set in the class defintion
# as class variables, making them avilable without having to create a class
# instance. This allows higher level logic to rapidly create a index of Qwiic
# devices at runtine
_DEFAULT_NAME = "Qwiic ISM330DHCX"

# Some devices have multiple available addresses - this is a list of these
# addresses. NOTE: The first address in this list is considered the default I2C
# address for the device.
_AVAILABLE_I2C_ADDRESS = [0x6B, 0x6A]

class IsmData:
    # Contains 3 axis data for storing either raw or calculated data from the ISM330DHCX
    def __init__(self):
        self.xData = 0
        self.yData = 0
        self.zData = 0

# Define the class that encapsulates the device being created. All information
# associated with this device is encapsulated by this class. The device class
# should be the only value exported from this module.
class QwiicISM330DHCX(object):
    # Set default name and I2C address(es)
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESS

    # Device identification
    kDevId = 0x6B
    kRegWhoAmI = 0x0F

    # Ctrl1 XL register
    kRegCtrl1XL = 0x10

    kCtrl1XlShiftOdr = 0
    kCtrl1XlMaskOdr = 0b1111 << kCtrl1XlShiftOdr
    kCtrl1XlShiftFs = 4
    kCtrl1XlMaskFs = 0b11 << kCtrl1XlShiftFs
    kCtrl1XlShiftLpf2XlEn = 6
    kCtrl1XlMaskLpf2XlEn = 0b1 << kCtrl1XlShiftLpf2XlEn

    kXlFs2g = 0
    kXlFs16g = 1
    kXlFs4g = 2
    kXlFs8g = 3
    
    # Ctrl2 G register
    kRegCtrl2G = 0x11
    kCtrl2GShiftOdr = 0
    kCtrl2GMaskOdr = 0b1111 << kCtrl2GShiftOdr
    kCtrl2GShiftFs = 4
    kCtrl2GMaskFs = 0b1111 << kCtrl2GShiftFs

    kGyroFs125dps = 2
    kGyroFs250dps = 0
    kGyroFs500dps = 4
    kGyroFs1000dps = 8
    kGyroFs2000dps = 12
    kGyroFs4000dps = 1

    # Temperature register
    kRegOutTempL = 0x20
    
    # Accelerometer and Gyro output registers
    kRegOutXLA = 0x28
    kRegOutXLG = 0x22

    # Configuration regs
    kRegFuncCfgAccess = 0x01
    kFuncCfgAccessShiftRegAccess = 0
    kFuncCfgAccessMaskRegAccess = 0b11 << kFuncCfgAccessShiftRegAccess

    kRegCtrl9XL = 0x18
    kCtrl9XlShiftDenX = 0
    kCtrl9XlMaskDenX = 0b1 << kCtrl9XlShiftDenX
    kCtrl9XlShiftDenY = 1
    kCtrl9XlMaskDenY = 0b1 << kCtrl9XlShiftDenY
    kCtrl9XlShiftDenZ = 2
    kCtrl9XlMaskDenZ = 0b1 << kCtrl9XlShiftDenZ
    kCtrl9XlShiftDenXlG = 3
    kCtrl9XlMaskDenXlG = 0b11 << kCtrl9XlShiftDenXlG
    kCtrl9XlShiftDenLh = 5
    kCtrl9XlMaskDenLh = 0b1 << kCtrl9XlShiftDenLh
    kCtrl9XlShiftDeviceConf = 6
    kCtrl9XlMaskDeviceConf = 0b1 << kCtrl9XlShiftDeviceConf

    kRegCtrl3C = 0x12
    kCtrl3CShiftBoot = 0
    kCtrl3CMaskBoot = 0b1 << kCtrl3CShiftBoot
    kCtrl3CShiftBdu = 1
    kCtrl3CMaskBdu = 0b1 << kCtrl3CShiftBdu
    kCtrl3CShiftHlActive = 2
    kCtrl3CMaskHlActive = 0b1 << kCtrl3CShiftHlActive
    kCtrl3CShiftPpOd = 3
    kCtrl3CMaskPpOd = 0b1 << kCtrl3CShiftPpOd
    kCtrl3CShiftSim = 4
    kCtrl3CMaskSim = 0b1 << kCtrl3CShiftSim
    kCtrl3CShiftIfInc = 5
    kCtrl3CMaskIfInc = 0b1 << kCtrl3CShiftIfInc
    kCtrl3CShiftSwReset = 7
    kCtrl3CMaskSwReset = 0b1 << kCtrl3CShiftSwReset

    kRegCtrl4C = 0x13
    kCtrl4CShiftSleepG = 1
    kCtrl4CMaskSleepG = 0b1 << kCtrl4CShiftSleepG
    kCtrl4CShiftInt2OnInt1 = 2
    kCtrl4CMaskInt2OnInt1 = 0b1 << kCtrl4CShiftInt2OnInt1
    kCtrl4CShiftDrdyMask = 4
    kCtrl4CMaskDrdyMask = 0b1 << kCtrl4CShiftDrdyMask
    kCtrl4CShiftI2cDisable = 5
    kCtrl4CMaskI2cDisable = 0b1 << kCtrl4CShiftI2cDisable
    kCtrl4CShiftLpf1SelG = 6
    kCtrl4CMaskLpf1SelG = 0b1 << kCtrl4CShiftLpf1SelG

    kRegCtrl6C = 0x15
    kCtrl6CShiftDenMode = 0
    kCtrl6CMaskDenMode = 0b111 << kCtrl6CShiftDenMode
    kCtrl6CShiftXlHmMode = 3
    kCtrl6CMaskXlHmMode = 0b1 << kCtrl6CShiftXlHmMode
    kCtrl6CShiftUsrOffW = 4
    kCtrl6CMaskUsrOffW = 0b1 << kCtrl6CShiftUsrOffW
    kCtrl6CShiftFtype = 5
    kCtrl6CMaskFtype = 0b111 << kCtrl6CShiftFtype

    kRegCtrl10C = 0x19
    kCtrl10CShiftTimestampEn = 2
    kCtrl10CMaskTimestampEn = 0b1 << kCtrl10CShiftTimestampEn

    kRegTimestamp0 = 0x40
    kRegTimestamp1 = 0x41
    kRegTimestamp2 = 0x42
    kRegTimestamp3 = 0x43

    # Slope Filtering
    kRegCtrl8XL = 0x17
    kCtrl8XlShiftHpcfXl = 0
    kCtrl8XlMaskHpcfXl = 0b111 << kCtrl8XlShiftHpcfXl
    kCtrl8XlShiftHpRefModeXl = 3
    kCtrl8XlMaskHpRefModeXl = 0b1 << kCtrl8XlShiftHpRefModeXl
    kCtrl8XlShiftFastSettlModeXl = 4
    kCtrl8XlMaskFastSettlModeXl = 0b1 << kCtrl8XlShiftFastSettlModeXl
    kCtrl8XlShiftHpSlopeXlEn = 5
    kCtrl8XlMaskHpSlopeXlEn = 0b1 << kCtrl8XlShiftHpSlopeXlEn
    kCtrl8XlShiftLowPassOn6d = 7
    kCtrl8XlMaskLowPassOn6d = 0b1 << kCtrl8XlShiftLowPassOn6d

    # Possilbe Slope Filters
    kHpPathDisableOnOut = 0x00
    kSlopeOdrDiv4 = 0x10
    kHpOdrDiv10 = 0x11
    kHpOdrDiv20 = 0x12
    kHpOdrDiv45 = 0x13
    kHpOdrDiv100 = 0x14
    kHpOdrDiv200 = 0x15
    kHpOdrDiv400 = 0x16
    kHpOdrDiv800 = 0x17
    kHpRefMdOdrDiv10 = 0x31
    kHpRefMdOdrDiv20 = 0x32
    kHpRefMdOdrDiv45 = 0x33
    kHpRefMdOdrDiv100 = 0x34
    kHpRefMdOdrDiv200 = 0x35
    kHpRefMdOdrDiv400 = 0x36
    kHpRefMdOdrDiv800 = 0x37
    kLpOdrDiv10 = 0x01
    kLpOdrDiv20 = 0x02
    kLpOdrDiv45 = 0x03
    kLpOdrDiv100 = 0x04
    kLpOdrDiv200 = 0x05
    kLpOdrDiv400 = 0x06
    kLpOdrDiv800 = 0x07

    # Possible bandwidths
    kBwUltraLight = 0
    kBwVeryLight = 1
    kBwLight = 2
    kBwMedium = 3
    kBwStrong = 4
    kBwVeryStrong = 5
    kBwAggressive = 6
    kBwXtreme = 7

    # Possible data rates (ODRs)
    # Accelerometer
    kXlOdrOff    = 0
    kXlOdr12Hz5  = 1
    kXlOdr26Hz   = 2
    kXlOdr52Hz   = 3
    kXlOdr104Hz  = 4
    kXlOdr208Hz  = 5
    kXlOdr416Hz  = 6
    kXlOdr833Hz  = 7
    kXlOdr1666Hz = 8
    kXlOdr3332Hz = 9
    kXlOdr6667Hz = 10
    kXlOdr1Hz6   = 11
    
    # Gyroscope
    kGyroOdrOff    = 0
    kGyroOdr12Hz5  = 1
    kGyroOdr26Hz   = 2
    kGyroOdr52Hz   = 3
    kGyroOdr104Hz  = 4
    kGyroOdr208Hz  = 5
    kGyroOdr416Hz  = 6
    kGyroOdr833Hz  = 7
    kGyroOdr1666Hz = 8
    kGyroOdr3332Hz = 9
    kGyroOdr6667Hz = 10

    # MLC
    kMlcOdr12Hz5 = 0
    kMlcOdr26Hz  = 1
    kMlcOdr52Hz  = 2
    kMlcOdr104Hz = 3

    # Sensor Hub
    kShOdr104Hz = 0
    kShOdr52Hz  = 1
    kShOdr26Hz  = 2
    kShOdr13Hz  = 3

    # Possible mem bank values
    kUserBank = 0
    kSensorHubBank = 1
    kEmbeddedFuncBank = 2

    kRegEmbFuncOdrCfgB = 0x5F
    kEmbFuncOdrShiftFsmOdr = 3
    kEmbFuncOdrMaskFsmOdr = 0b11 << kEmbFuncOdrShiftFsmOdr

    kOdrFsm12Hz5 = 0
    kOdrFsm26Hz  = 1
    kOdrFsm52Hz  = 2
    kOdrFsm104Hz = 3

    kRegEmbFuncEnB = 0x05
    kEmbFuncEnBShiftMlcEn = 3
    kEmbFuncEnBMaskMlcEn = 0b1 << kEmbFuncEnBShiftMlcEn
    kEmbFuncEnBShiftFifoComprEn = 4
    kEmbFuncEnBMaskFifoComprEn = 0b1 << kEmbFuncEnBShiftFifoComprEn
    kEmbFuncEnBShiftFsmEn = 7
    kEmbFuncEnBMaskFsmEn = 0b1 << kEmbFuncEnBShiftFsmEn

    kRegEmbFuncOdrCfgC = 0x60
    kEmbFuncOdrShiftMlcOdr = 2
    kEmbFuncOdrMaskMlcOdr = 0b11 << kEmbFuncOdrShiftMlcOdr

    # Fifo Registers
    kRegFifoCtrl1 = 0x07

    kRegFifoCtrl2 = 0x08
    kFifoCtrl2ShiftStopOnWtm = 0
    kFifoCtrl2MaskStopOnWtm = 0b1 << kFifoCtrl2ShiftStopOnWtm
    kFifoCtrl2ShiftFifoComprRtEn = 1
    kFifoCtrl2MaskFifoComprRtEn = 0b1 << kFifoCtrl2ShiftFifoComprRtEn
    kFifoCtrl2ShiftOdrChgEn = 3
    kFifoCtrl2MaskOdrChgEn = 0b1 << kFifoCtrl2ShiftOdrChgEn
    kFifoCtrl2ShiftUncoptrRate = 5
    kFifoCtrl2MaskUncoptrRate = 0b11 << kFifoCtrl2ShiftUncoptrRate
    kFifoCtrl2ShiftWtm = 7
    kFifoCtrl2MaskWtm = 0b1 << kFifoCtrl2ShiftWtm

    kRegFifoCtrl3 = 0x09
    kFifoCtrl3ShiftBdrGy = 0
    kFifoCtrl3MaskBdrGy = 0b1111 << kFifoCtrl3ShiftBdrGy
    kFifoCtrl3ShiftBdrXl = 4
    kFifoCtrl3MaskBdrXl = 0b1111 << kFifoCtrl3ShiftBdrXl

    kRegFifoCtrl4 = 0x0A
    kFifoCtrl4ShiftOdrTsBatch = 0
    kFifoCtrl4MaskOdrTsBatch = 0b11 << kFifoCtrl4ShiftOdrTsBatch
    kFifoCtrl4ShiftOdrTBatch = 2
    kFifoCtrl4MaskOdrTBatch = 0b11 << kFifoCtrl4ShiftOdrTBatch
    kFifoCtrl4ShiftFifoMode = 5
    kFifoCtrl4MaskFifoMode = 0b111 << kFifoCtrl4ShiftFifoMode


    # Possible Fifo Modes
    kBypassMode = 0
    kFifoMode = 1
    kStreamToFifoMode = 3
    kBypassToStreamMode = 4
    kStreamMode = 6
    kBypassToFifoMode = 7

    # Possible Accelerometer Batch Data Rates
    kXlNotBatched = 0
    kXlBatchedAt12Hz5 = 1
    kXlBatchedAt26Hz = 2
    kXlBatchedAt52Hz = 3
    kXlBatchedAt104Hz = 4
    kXlBatchedAt208Hz = 5
    kXlBatchedAt417Hz = 6
    kXlBatchedAt833Hz = 7
    kXlBatchedAt1667Hz = 8
    kXlBatchedAt3333Hz = 9
    kXlBatchedAt6667Hz = 10
    kXlBatchedAt6Hz5 = 11

    # Possible Gyroscope Batch Data Rates
    kGyroNotBatched = 0
    kGyroBatchedAt12Hz5 = 1
    kGyroBatchedAt26Hz = 2
    kGyroBatchedAt52Hz = 3
    kGyroBatchedAt104Hz = 4
    kGyroBatchedAt208Hz = 5
    kGyroBatchedAt417Hz = 6
    kGyroBatchedAt833Hz = 7
    kGyroBatchedAt1667Hz = 8
    kGyroBatchedAt3333Hz = 9
    kGyroBatchedAt6667Hz = 10
    kGyroBatchedAt6Hz5 = 11

    # Possible Decimation Rates
    kNoDecimation = 0
    kDec1 = 1
    kDec8 = 2
    kDec32 = 3

    # Possible Interrupt Events
    kAllIntPulsed = 0
    kBaseLatchedEmbPulsed = 1
    kBasePulsedEmbLatched = 2
    kAllIntLatched = 3

    # Interrupt configuration
    kRegTapCfg0 = 0x56
    kTapCfg0ShiftIntClrOnRead = 1
    kTapCfg0MaskIntClrOnRead = 0b1 << kTapCfg0ShiftIntClrOnRead
    kTapCfg0ShiftSleepStatusOnInt = 2
    kTapCfg0MaskSleepStatusOnInt = 0b1 << kTapCfg0ShiftSleepStatusOnInt
    kTapCfg0ShiftSlopeFds = 3
    kTapCfg0MaskSlopeFds = 0b1 << kTapCfg0ShiftSlopeFds
    kTapCfg0ShiftTapXEn = 4
    kTapCfg0MaskTapXEn = 0b1 << kTapCfg0ShiftTapXEn
    kTapCfg0ShiftTapYEn = 5
    kTapCfg0MaskTapYEn = 0b1 << kTapCfg0ShiftTapYEn
    kTapCfg0ShiftTapZEn = 6
    kTapCfg0MaskTapZEn = 0b1 << kTapCfg0ShiftTapZEn
    kTapCfg0ShiftLir = 7
    kTapCfg0MaskLir = 0b1 << kTapCfg0ShiftLir

    kRegTapCfg2 = 0x58
    kTapCfg2ShiftInterruptsEnable = 0
    kTapCfg2MaskInterruptsEnable = 0b1 << kTapCfg2ShiftInterruptsEnable
    kTapCfg2ShiftInactEn = 1
    kTapCfg2MaskInactEn = 0b11 << kTapCfg2ShiftInactEn
    kTapCfg2ShiftTapThsY = 3
    kTapCfg2MaskTapThsY = 0b11111 << kTapCfg2ShiftTapThsY

    kRegPageRw = 0x17
    kPageRwShiftEmbFuncLir = 0
    kPageRwMaskEmbFuncLir = 0b1 << kPageRwShiftEmbFuncLir
    kPageRwShiftPageRw = 1
    kPageRwMaskPageRw = 0b11 << kPageRwShiftPageRw

    kRegMlcInt1 = 0x0D

    kRegEmbFuncInt1 = 0x0A
    kEmbFuncInt1ShiftFsmLc = 0
    kEmbFuncInt1MaskFsmLc = 0b1 << kEmbFuncInt1ShiftFsmLc
    kEmbFuncInt1ShiftSigMot = 1
    kEmbFuncInt1MaskSigMot = 0b1 << kEmbFuncInt1ShiftSigMot
    kEmbFuncInt1ShiftTilt = 2
    kEmbFuncInt1MaskTilt = 0b1 << kEmbFuncInt1ShiftTilt
    kEmbFuncInt1ShiftStepDetector = 3
    kEmbFuncInt1MaskStepDetector = 0b1 << kEmbFuncInt1ShiftStepDetector

    kRegFsmInt1A = 0x0B
    kRegFsmInt1B = 0x0C

    kRegInt1Ctrl = 0x0D
    kInt1CtrlShiftDenDrdyFlag = 0
    kInt1CtrlMaskDenDrdyFlag = 0b1 << kInt1CtrlShiftDenDrdyFlag
    kInt1CtrlShiftInt1CntBdr = 1
    kInt1CtrlMaskInt1CntBdr = 0b1 << kInt1CtrlShiftInt1CntBdr
    kInt1CtrlShiftInt1FifoFull = 2
    kInt1CtrlMaskInt1FifoFull = 0b1 << kInt1CtrlShiftInt1FifoFull
    kInt1CtrlShiftInt1FifoOvr = 3
    kInt1CtrlMaskInt1FifoOvr = 0b1 << kInt1CtrlShiftInt1FifoOvr
    kInt1CtrlShiftInt1FifoTh = 4
    kInt1CtrlMaskInt1FifoTh = 0b1 << kInt1CtrlShiftInt1FifoTh
    kInt1CtrlShiftInt1Boot = 5
    kInt1CtrlMaskInt1Boot = 0b1 << kInt1CtrlShiftInt1Boot
    kInt1CtrlShiftInt1DrdyG = 6
    kInt1CtrlMaskInt1DrdyG = 0b1 << kInt1CtrlShiftInt1DrdyG
    kInt1CtrlShiftInt1DrdyXl = 7
    kInt1CtrlMaskInt1DrdyXl = 0b1 << kInt1CtrlShiftInt1DrdyXl

    kRegMd1Cfg = 0x5E
    kMd1CfgShiftInt1SleepChange = 0
    kMd1CfgMaskInt1SleepChange = 0b1 << kMd1CfgShiftInt1SleepChange
    kMd1CfgShiftInt1SingleTap = 1
    kMd1CfgMaskInt1SingleTap = 0b1 << kMd1CfgShiftInt1SingleTap
    kMd1CfgShiftInt1Wu = 2
    kMd1CfgMaskInt1Wu = 0b1 << kMd1CfgShiftInt1Wu
    kMd1CfgShiftInt1Ff = 3
    kMd1CfgMaskInt1Ff = 0b1 << kMd1CfgShiftInt1Ff
    kMd1CfgShiftInt1DoubleTap = 4
    kMd1CfgMaskInt1DoubleTap = 0b1 << kMd1CfgShiftInt1DoubleTap
    kMd1CfgShiftInt16d = 5
    kMd1CfgMaskInt16d = 0b1 << kMd1CfgShiftInt16d
    kMd1CfgShiftInt1EmbFunc = 6
    kMd1CfgMaskInt1EmbFunc = 0b1 << kMd1CfgShiftInt1EmbFunc
    kMd1CfgShiftInt1Shub = 7
    kMd1CfgMaskInt1Shub = 0b1 << kMd1CfgShiftInt1Shub


    kRegEmbFunInt2 = 0x0E
    kEmbFuncInt2ShiftFsmLc = 0
    kEmbFuncInt2MaskFsmLc = 0b1 << kEmbFuncInt2ShiftFsmLc
    kEmbFuncInt2ShiftSigMot = 2
    kEmbFuncInt2MaskSigMot = 0b1 << kEmbFuncInt2ShiftSigMot
    kEmbFuncInt2ShiftTilt = 3
    kEmbFuncInt2MaskTilt = 0b1 << kEmbFuncInt2ShiftTilt
    kEmbFuncInt2ShiftStepDetector = 4
    kEmbFuncInt2MaskStepDetector = 0b1 << kEmbFuncInt2ShiftStepDetector

    kRegFsmInt2A = 0x0F
    kRegFsmInt2B = 0x10
    kRegMlcInt2 = 0x11

    kRegInt2Ctrl = 0x0E
    kInt2CtrlShiftInt2CntBdr = 1
    kInt2CtrlMaskInt2CntBdr = 0b1 << kInt2CtrlShiftInt2CntBdr
    kInt2CtrlShiftInt2FifoFull = 2
    kInt2CtrlMaskInt2FifoFull = 0b1 << kInt2CtrlShiftInt2FifoFull
    kInt2CtrlShiftInt2FifoOvr = 3
    kInt2CtrlMaskInt2FifoOvr = 0b1 << kInt2CtrlShiftInt2FifoOvr
    kInt2CtrlShiftInt2FifoTh = 4
    kInt2CtrlMaskInt2FifoTh = 0b1 << kInt2CtrlShiftInt2FifoTh
    kInt2CtrlShiftInt2DrdyTemp = 5
    kInt2CtrlMaskInt2DrdyTemp = 0b1 << kInt2CtrlShiftInt2DrdyTemp
    kInt2CtrlShiftInt2DrdyG = 6
    kInt2CtrlMaskInt2DrdyG = 0b1 << kInt2CtrlShiftInt2DrdyG
    kInt2CtrlShiftInt2DrdyXl = 7
    kInt2CtrlMaskInt2DrdyXl = 0b1 << kInt2CtrlShiftInt2DrdyXl

    kRegMd2Cfg = 0x5F
    kMd2CfgShiftInt2SleepChange = 0
    kMd2CfgMaskInt2SleepChange = 0b1 << kMd2CfgShiftInt2SleepChange
    kMd2CfgShiftInt2SingleTap = 1
    kMd2CfgMaskInt2SingleTap = 0b1 << kMd2CfgShiftInt2SingleTap
    kMd2CfgShiftInt2Wu = 2
    kMd2CfgMaskInt2Wu = 0b1 << kMd2CfgShiftInt2Wu
    kMd2CfgShiftInt2Ff = 3
    kMd2CfgMaskInt2Ff = 0b1 << kMd2CfgShiftInt2Ff
    kMd2CfgShiftInt2DoubleTap = 4
    kMd2CfgMaskInt2DoubleTap = 0b1 << kMd2CfgShiftInt2DoubleTap
    kMd2CfgShiftInt26d = 5
    kMd2CfgMaskInt26d = 0b1 << kMd2CfgShiftInt26d
    kMd2CfgShiftInt2EmbFunc = 6
    kMd2CfgMaskInt2EmbFunc = 0b1 << kMd2CfgShiftInt2EmbFunc
    kMd2CfgShiftInt2Timestamp = 7
    kMd2CfgMaskInt2Timestamp = 0b1 << kMd2CfgShiftInt2Timestamp

    kRegSlv0Config = 0x17
    kSlv0ConfigShiftShubOdr = 0
    kSlv0ConfigMaskShubOdr = 0b11 << kSlv0ConfigShiftShubOdr
    kSlv0ConfigShiftBatchExtSens0En = 4
    kSlv0ConfigMaskBatchExtSens0En = 0b1 << kSlv0ConfigShiftBatchExtSens0En
    kSlv0ConfigShiftSlave0Numop = 5
    kSlv0ConfigMaskSlave0Numop = 0b111 << kSlv0ConfigShiftSlave0Numop

    # Data Ready Pulse modes
    kDrdyLatched = 0
    kDrdyPulsed = 1

    kRegCntrBdr1 = 0x0B
    kCntrBdr1ShiftDatareadyPulsed = 0
    kCntrBdr1MaskDatareadyPulsed = 0b1 << kCntrBdr1ShiftDatareadyPulsed
    kCntrBdr1ShiftRstCounterBdr = 1
    kCntrBdr1MaskRstCounterBdr = 0b1 << kCntrBdr1ShiftRstCounterBdr
    kCntrBdr1ShiftTrigCounterBdr = 2
    kCntrBdr1MaskTrigCounterBdr = 0b1 << kCntrBdr1ShiftTrigCounterBdr
    kCntrBdr1ShiftCntBdrTh = 5
    kCntrBdr1MaskCntBdrTh = 0b111 << kCntrBdr1ShiftCntBdrTh


    def __init__(self, address=None, i2c_driver=None):
        """
        Constructor

        :param address: The I2C address to use for the device
            If not provided, the default address is used
        :type address: int, optional
        :param i2c_driver: An existing i2c driver object
            If not provided, a driver object is created
        :type i2c_driver: I2CDriver, optional
        """

        # Use address if provided, otherwise pick the default
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]

        # Load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver

        self._fullScaleAccel = 0 # powered down by default
        self._fullScaleGyro = 0  # powered down by default

    def is_connected(self):
        """
        Determines if this device is connected

        :return: `True` if connected, otherwise `False`
        :rtype: bool
        """
        
        if self._i2c.isDeviceConnected(self.address) == False:
            return False
        
        # Confirm device ID is correct
        if self.get_id() != self.kDevId:
            return False
        
    connected = property(is_connected)

    def begin(self):
        """
        Initializes this device with default parameters

        :return: Returns `True` if successful, otherwise `False`
        :rtype: bool
        """
        # Confirm device is connected before doing anything
        return self.is_connected()

    def get_id(self):
        """
        Get the device ID

        :return: The device ID
        :rtype: int
        """
        return self._i2c.readByte(self.address, self.kRegWhoAmI)

    def set_accel_full_scale(self, val):
        """
        Set the scale of the accelerometer's readings 2g - 16g

        :param val: The scale to be applied to the accelerometer (0 - 3)
        :type val: int

        Possible values:
            - kXlFs2g
            - kXlFs16g
            - kXlFs4g
            - kXlFs8g
        """
        if val < self.kXlFs2g or val > self.kXlFs8g:
            return

        regVal = self._i2c.readByte(self.address, self.kRegCtrl1XL)

        regVal &= ~self.kCtrl1XlMaskFs
        regVal |= (val << self.kCtrl1XlShiftFs)

        self._i2c.writeByte(self.address, self.kRegCtrl1XL, regVal)

        self._fullScaleAccel = val
    
    def set_gyro_full_scale(self, val):
        """
        Set the scale of the gyroscope's readings 125, 250, 500, 1000, 2000, 4000 degrees per second

        :param val: The scale to be applied to the gyroscope (0, 1, 2, 4, 6, 12)
        :type val: int
        """
        if val < self.kGyroFs125dps or val > self.kGyroFs4000dps:
            return

        regVal = self._i2c.readByte(self.address, self.kRegCtrl2G)

        regVal &= ~self.kCtrl2GMaskFs
        regVal |= (val << self.kCtrl2GShiftFs)

        self._i2c.writeByte(self.address, self.kRegCtrl2G, regVal)

        self._fullScaleGyro = val

    def get_accel_full_scale(self):
        """
        Get the scale of the accelerometer's readings

        :return: The scale of the accelerometer's readings
        :rtype: int

        Possible return values:
            - kXlFs2g
            - kXlFs16g
            - kXlFs4g
            - kXlFs8g
        """
        regVal = self._i2c.readByte(self.address, self.kRegCtrl1XL)

        return (regVal & self.kCtrl1XlMaskFs) >> self.kCtrl1XlShiftFs


    def get_gyro_full_scale(self):
        """
        Get the scale of the gyroscope's readings

        :return: The scale of the gyroscope's readings
        :rtype: int

        Possible return values:
            - kGyroFs125dps
            - kGyroFs250dps
            - kGyroFs500dps
            - kGyroFs1000dps
            - kGyroFs2000dps
            - kGyroFs4000dps
        """
        regVal = self._i2c.readByte(self.address, self.kRegCtrl2G)

        return (regVal & self.kCtrl2GMaskFs) >> self.kCtrl2GShiftFs

    def get_temp(self):
        """
        Get the temperature

        :return: The temperature in degrees Celsius
        :rtype: float
        """
        temp = self._i2c.read_block(self.address, self.kRegOutTempL)
        val = (temp[1] << 8) | temp[0]
        # Convert to from unsigned to signed 16-bit
        if val > 32767:
            val -= 65536
        
        return val

    def _get_raw_data(self, reg):
        """
        Get the raw data from the specified register
        
        :param reg: The register to read from
        :type reg: int
        """
        bytes = self._i2c.read_block(self.address, reg)

        dataOut = IsmData()
        dataOut.xData = (bytes[1] << 8) | bytes[0]
        dataOut.yData = (bytes[3] << 8) | bytes[2]
        dataOut.zData = (bytes[5] << 8) | bytes[4]

        # Convert to signed 16-bit
        dataOut.xData, dataOut.yData, dataOut.zData = [
            val if val < 32768 else val - 65536 for val in [dataOut.xData, dataOut.yData, dataOut.zData]
        ]

        return dataOut

    def get_raw_accel(self):
        """
        Get the raw accelerometer readings

        :return: The raw accelerometer readings
        :rtype: list
        """
        return self._get_raw_data(self.kRegOutXLA)
    
    def get_raw_gyro(self):
        """
        Get the raw gyroscope readings

        :return: The raw gyroscope readings
        :rtype: list
        """
        return self._get_raw_data(self.kRegOutXLG)

    def _convert_data(self, data, key, convDict):
        """
        Use the key parameter to extract the conversion function from convDict and apply it to the data

        :param data: The data to be converted
        :type data: IsmData

        :param key: The key to be used to extract the conversion function from convDict
        :type key: int

        :param convDict: The dictionary containing the conversion functions
        :type convDict: dict

        :return: The converted data
        :rtype: IsmData
        """
        if key in convDict:
            conv = convDict[key]
            data.xData = conv(data.xData)
            data.yData = conv(data.yData)
            data.zData = conv(data.zData)
        else:
            return None

        return data

    def get_accel(self):
        """
        Retrieves raw register values and converts them according to the full scale settings

        :return: The accelerometer data in mg
        :rtype: IsmData
        """
        data = self.get_raw_accel()

        fullScaleConversions = {
            self.kXlFs2g: self.convert_2g_to_mg,
            self.kXlFs4g: self.convert_4g_to_mg,
            self.kXlFs8g: self.convert_8g_to_mg,
            self.kXlFs16g: self.convert_16g_to_mg
        }

        return self._convert_data(data, self._fullScaleAccel, fullScaleConversions)

    def get_gyro(self):
        """
        Retrieves raw register values and converts them according to the full scale settings

        :return: The gyroscope data in mdps
        :rtype: IsmData
        """
        data = self.get_raw_gyro()

        fullScaleConversions = {
            self.kGyroFs125dps: self.convert_125dps_to_mdps,
            self.kGyroFs250dps: self.convert_250dps_to_mdps,
            self.kGyroFs500dps: self.convert_500dps_to_mdps,
            self.kGyroFs1000dps: self.convert_1000dps_to_mdps,
            self.kGyroFs2000dps: self.convert_2000dps_to_mdps,
            self.kGyroFs4000dps: self.convert_4000dps_to_mdps
        }

        return self._convert_data(data, self._fullScaleGyro, fullScaleConversions)

    # Conversion functions
    def convert_2g_to_mg(self, lsb):
        return lsb * 0.061

    def convert_4g_to_mg(self, lsb):
        return lsb * 0.122

    def convert_8g_to_mg(self, lsb):
        return lsb * 0.244

    def convert_16g_to_mg(self, lsb):
        return lsb * 0.488

    def convert_125dps_to_mdps(self, lsb):
        return lsb * 4.375

    def convert_250dps_to_mdps(self, lsb):
        return lsb * 8.75

    def convert_500dps_to_mdps(self, lsb):
        return lsb * 17.50

    def convert_1000dps_to_mdps(self, lsb):
        return lsb * 35.0

    def convert_2000dps_to_mdps(self, lsb):
        return lsb * 70.0

    def convert_4000dps_to_mdps(self, lsb):
        return lsb * 140.0

    def convert_lsb_to_celsius(self, lsb):
        return (lsb / 256.0) + 25.0

    def convert_lsb_to_nsec(self, lsb):
        return lsb * 25000.0

    def set_device_config(self, enable):
        """
        Enable the general device configuration
        
        :param enable: Enable or disable the device configuration
        :type enable: bool
        """
        if enable != 0 and enable != 1:
            return
        
        val = self._i2c.readByte(self.address, self.kRegCtrl9XL)
        
        val &= ~self.kCtrl9XlMaskDeviceConf
        val |= (enable << self.kCtrl9XlShiftDeviceConf)

        self._i2c.writeByte(self.address, self.kRegCtrl9XL, val)

    def device_reset(self):
        """
        Reset the device to default settings
        """
        val = self._i2c.readByte(self.address, self.kRegCtrl3C)
        
        val |= self.kCtrl3CMaskSwReset

        self._i2c.writeByte(self.address, self.kRegCtrl3C, val)

    def get_device_reset(self):
        """
        Get the device reset state

        :return: The device reset state
        :rtype: bool
        """
        val = self._i2c.readByte(self.address, self.kRegCtrl3C)

        return bool(val & self.kCtrl3CMaskSwReset)

    def set_accel_slope_filter(self, val):
        """
        Set's the accelerometer's slope filter

        :param val: The intensity of the filter (0x00 - 0x37)
        :type val: int

        See the constants in the class definition under "Possilbe Slope Filters" for a list of valid arguments
        """
        if val < self.kHpPathDisableOnOut or val > self.kHpRefMdOdrDiv800:
            return
        

        newSlopeEn = (val & 0x10) >> 4
        newRefMode = (val & 0x20) >> 5
        newCf = (val & 0x07)

        regVal = self._i2c.readByte(self.address, self.kRegCtrl8XL)

        regVal &= ~self.kCtrl8XlMaskHpSlopeXlEn
        regVal |= (newSlopeEn << self.kCtrl8XlShiftHpSlopeXlEn)

        regVal &= ~self.kCtrl8XlMaskHpRefModeXl
        regVal |= (newRefMode << self.kCtrl8XlShiftHpRefModeXl)

        regVal &= ~self.kCtrl8XlMaskHpcfXl
        regVal |= (newCf << self.kCtrl8XlShiftHpcfXl)
        
        self._i2c.writeByte(self.address, self.kRegCtrl8XL, regVal)
    
    def set_accel_filter_lp2(self, enable):
        """
        Enable the accelerometer's high resolution slope filter
        
        :param enable: Enable or disable the filter
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.readByte(self.address, self.kRegCtrl1XL)
        
        val &= ~self.kCtrl1XlMaskLpf2XlEn
        val |= (enable << self.kCtrl1XlShiftLpf2XlEn)

        self._i2c.writeByte(self.address, self.kRegCtrl1XL, val)

    def set_gyro_filter_lp1(self, enable):
        """
        Enables the gyroscope's slope filter

        :param enable: Enable or disable the filter
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.readByte(self.address, self.kRegCtrl4C)

        val &= ~self.kCtrl4CMaskLpf1SelG
        val |= (enable << self.kCtrl4CShiftLpf1SelG)

        self._i2c.writeByte(self.address, self.kRegCtrl4C, val)
        
    def set_gyro_lp1_bandwidth(self, val):
        """
        Sets the low pass filter's bandwidth for the gyroscope
        
        :param val: The bandwidth of the filter
        :type val: int

        Possible values:
            - kBwUltraLight
            - kBwVeryLight
            - kBwLight
            - kBwMedium
            - kBwStrong
            - kBwVeryStrong
            - kBwAggressive
            - kBwXtreme
        """
        if val < self.kBwUltraLight or val > self.kBwXtreme:
            return
        
        regVal = self._i2c.readByte(self.address, self.kRegCtrl6C)

        regVal &= ~self.kCtrl6CMaskFtype
        regVal |= (val << self.kCtrl6CShiftFtype)

        self._i2c.writeByte(self.address, self.kRegCtrl6C, regVal)

    def set_block_data_update(self, enable):
        """
        Data is not updated until both MSB and LSB have been read from output registers

        :param enable: Enable or disable the block data update
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.readByte(self.address, self.kRegCtrl3C)

        val &= ~self.kCtrl3CMaskBdu
        val |= (enable << self.kCtrl3CShiftBdu)

        self._i2c.writeByte(self.address, self.kRegCtrl3C, val)

    def get_block_data_update(self):
        """
        Retrieves the bit indicating if block data update is enabled

        :return: The block data update state
        :rtype: int
        """
        val = self._i2c.readByte(self.address, self.kRegCtrl3C)

        return (val & self.kCtrl3CMaskBdu) >> self.kCtrl3CShiftBdu
    
    def _mem_bank_set(self, val):
        """
        Enable access to the embedded functions/sensor hub configuration registers. Not to be used outside this module

        :param val: The value to set the memory bank to
        :type val: int

        Possible values:
            - kUserBank
            - kSensorHubBank
            - kEmbeddedFuncBank
        """
        if val < self.kUserBank or val > self.kEmbeddedFuncBank:
            return

        regVal = self._i2c.readByte(self.address, self.kRegFuncCfgAccess)

        regVal &= ~self.kFuncCfgAccessMaskRegAccess
        regVal |= (val << self.kFuncCfgAccessShiftRegAccess)

        self._i2c.writeByte(self.address, self.kRegFuncCfgAccess, regVal)

    def _fsm_enable_get(self):
        """
        Embedded finite state machine functions mode. Not to be used outside this module

        :return: Tuple containing fsmEnableA followed by fsmEnableB
        :rtype: tuple of int
        """
        self._mem_bank_set(self.kEmbeddedFuncBank)

        fsmEnableA = self._i2c.readByte(self.address, self.kRegFsmEnableA)
        fsmEnableB = self._i2c.readByte(self.address, self.kRegFsmEnableB)

        self._mem_bank_set(self.kUserBank)

        return (fsmEnableA, fsmEnableB)
    
    def _fsm_data_rate_get(self):
        """
        Get the data rate (ODR) of the finite state machine

        :return: The data rate of the finite state machine
        :rtype: int

        Possible return values:
            - kOdrFsm12Hz5
            - kOdrFsm26Hz
            - kOdrFsm52Hz
            - kOdrFsm104Hz
        """
        self._mem_bank_set(self.kEmbeddedFuncBank)

        fsmOdrCfgB = self._i2c.readByte(self.address, self.kRegEmbFuncOdrCfgB)

        self._mem_bank_set(self.kUserBank)

        return (fsmOdrCfgB & self.kEmbFuncOdrMaskFsmOdr) >> self.kEmbFuncOdrShiftFsmOdr
    
    def _mlc_get(self):
        """
        Get the Machine Learning Core enable state

        :return: The Machine Learning Core enable state
        :rtype: int
        """
        self._mem_bank_set(self.kEmbeddedFuncBank)

        regVal = self._i2c.readByte(self.address, self.kRegEmbFuncEnB)

        self._mem_bank_set(self.kUserBank)

        return (regVal & self.kEmbFuncEnBMaskMlcEn) >> self.kEmbFuncEnBShiftMlcEn
    
    def _mlc_data_rate_get(self):
        """
        Get Machine Learning Core data rate selection
        
        :return: The Machine Learning Core data rate selection
        :rtype: int

        For possible return values see the "MLC" section in "Possible data rates" in the class definition
        """
        self._mem_bank_set(self.kEmbeddedFuncBank)

        regVal = self._i2c.readByte(self.address, self.kRegEmbFuncOdrCfgC)

        self._mem_bank_set(self.kUserBank)

        return (regVal & self.kEmbFuncOdrMaskMlcOdr) >> self.kEmbFuncOdrShiftMlcOdr


    def set_accel_data_rate(self, val): 
        """
        Sets the data output rate of the accelerometer

        :param val: Data rate
        :type val: int

        See the "Accelerometer section in Possible data rates" in the class definition for a list of valid arguments
        """
        if val < self.kXlOdrOff or val > self.kXlOdr1Hz6:
            return
        
        enableA, enableB = self._fsm_enable_get()

        odrXl = val

        if (enableA & 0xFF) or (enableB & 0xFF):
            # Coresponds to any of the FSMs being enabled
            fsmOdr = self._fsm_data_rate_get()
            if fsmOdr == self.kOdrFsm12Hz5:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr12Hz5

            elif fsmOdr == self.kOdrFsm26Hz:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr26Hz
                elif val == self.kXlOdr12Hz5:
                    odrXl = self.kXlOdr26Hz

            elif fsmOdr == self.kOdrFsm52Hz:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr52Hz
                elif val == self.kXlOdr12Hz5:
                    odrXl = self.kXlOdr52Hz
                elif val == self.kXlOdr26Hz:
                    odrXl = self.kXlOdr52Hz

            elif fsmOdr == self.kOdrFsm104Hz:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr104Hz
                elif val == self.kXlOdr12Hz5:
                    odrXl = self.kXlOdr104Hz
                elif val == self.kXlOdr26Hz:
                    odrXl = self.kXlOdr104Hz
                elif val == self.kXlOdr52Hz:
                    odrXl = self.kXlOdr104Hz

        # Machine Learning Core data rate constraints:
        mlcEnable = self._mlc_get()

        if mlcEnable:
            mlc_odr = self._mlc_data_rate_get()

            if mlc_odr == self.kMlcOdr12Hz5:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr12Hz5
                else:
                    odrXl = val

            elif mlc_odr == self.kMlcOdr26Hz:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr26Hz
                elif val == self.kXlOdr12Hz5:
                    odrXl = self.kXlOdr26Hz
                else:
                    odrXl = val

            elif mlc_odr == self.kMlcOdr52Hz:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr52Hz
                elif val == self.kXlOdr12Hz5:
                    odrXl = self.kXlOdr52Hz
                elif val == self.kXlOdr26Hz:
                    odrXl = self.kXlOdr52Hz
                else:
                    odrXl = val

            elif mlc_odr == self.kMlcOdr104Hz:
                if val == self.kXlOdrOff:
                    odrXl = self.kXlOdr104Hz
                elif val == self.kXlOdr12Hz5:
                    odrXl = self.kXlOdr104Hz
                elif val == self.kXlOdr26Hz:
                    odrXl = self.kXlOdr104Hz
                elif val == self.kXlOdr52Hz:
                    odrXl = self.kXlOdr104Hz
                else:
                    odrXl = val

            else:
                odrXl = val

        regVal = self._i2c.readByte(self.address, self.kRegCtrl1XL)

        regVal &= ~self.kCtrl1XlMaskOdrXl
        regVal |= (odrXl << self.kCtrl1XlShiftOdrXl)

        self._i2c.writeByte(self.address, self.kRegCtrl1XL, regVal)

    def set_gyro_data_rate(self, val):
        """
        Sets the data output rate of the gyroscope

        :param val: Data rate
        :type val: int

        See the "Gyroscope" section in Possible data rates" in the class definition for a list of valid arguments
        """
        if val < self.kGyroOdrOff or val > self.kGyroOdr6667Hz:
            return
        
        enableA, enableB = self._fsm_enable_get()

        odrGy = val

        if (enableA & 0xFF) or (enableB & 0xFF):
            # Coresponds to any of the FSMs being enabled
            fsmOdr = self._fsm_data_rate_get()
            if fsmOdr == self.kOdrFsm12Hz5:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr12Hz5

            elif fsmOdr == self.kOdrFsm26Hz:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr26Hz
                elif val == self.kGyroOdr12Hz5:
                    odrGy = self.kGyroOdr26Hz

            elif fsmOdr == self.kOdrFsm52Hz:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr52Hz
                elif val == self.kGyroOdr12Hz5:
                    odrGy = self.kGyroOdr52Hz
                elif val == self.kGyroOdr26Hz:
                    odrGy = self.kGyroOdr52Hz

            elif fsmOdr == self.kOdrFsm104Hz:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr104Hz
                elif val == self.kGyroOdr12Hz5:
                    odrGy = self.kGyroOdr104Hz
                elif val == self.kGyroOdr26Hz:
                    odrGy = self.kGyroOdr104Hz
                elif val == self.kGyroOdr52Hz:
                    odrGy = self.kGyroOdr104Hz
        
        mlcEnable = self._mlc_get()
        if mlcEnable:
            mlc_odr = self._mlc_data_rate_get()
            if mlc_odr == self.kMlcOdr12Hz5:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr12Hz5
                else:
                    odrGy = val

            elif mlc_odr == self.kMlcOdr26Hz:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr26Hz
                elif val == self.kGyroOdr12Hz5:
                    odrGy = self.kGyroOdr26Hz
                else:
                    odrGy = val

            elif mlc_odr == self.kMlcOdr52Hz:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr52Hz
                elif val == self.kGyroOdr12Hz5:
                    odrGy = self.kGyroOdr52Hz
                elif val == self.kGyroOdr26Hz:
                    odrGy = self.kGyroOdr52Hz
                else:
                    odrGy = val

            elif mlc_odr == self.kMlcOdr104Hz:
                if val == self.kGyroOdrOff:
                    odrGy = self.kGyroOdr104Hz
                elif val == self.kGyroOdr12Hz5:
                    odrGy = self.kGyroOdr104Hz
                elif val == self.kGyroOdr26Hz:
                    odrGy = self.kGyroOdr104Hz
                elif val == self.kGyroOdr52Hz:
                    odrGy = self.kGyroOdr104Hz
                else:
                    odrGy = val

            else:
                odrGy = val
        
        regVal = self._i2c.readByte(self.address, self.kRegCtrl2G)

        regVal &= ~self.kCtrl2GMaskOdr
        regVal |= (odrGy << self.kCtrl2GShiftOdr)

        self._i2c.writeByte(self.address, self.kRegCtrl2G, regVal)


    def enable_timestamp(self, enable):
        """
        Enables the timestamp counter.
        
        :param enable: Enable or disable the timestamp counter
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        val = self._i2c.readByte(self.address, self.kRegCtrl10C)

        val &= ~self.kCtrl10CMaskTimestampEn
        val |= (enable << self.kCtrl10CShiftTimestampEn)

        self._i2c.writeByte(self.address, self.kRegCtrl10C, val)
    
    def reset_timestamp(self):
        """
        Resets the timestamp counter
        """
        resetVal = 0xAA
        self._i2c.writeByte(self.address, self.kRegTimestamp2, resetVal)

    # Fifo Methods
    def set_fifo_watermark(self, val):
        """
        Set the FIFO watermark level

        :param val: The watermark level. Must be between 0 and 511 (a 9-bit value)
        :type val: int
        """
        if val < 0 or val > 511:
            return
        
        ctrl2Val = (val >> 8) & 0x01 # WTM8
        ctrl1Val = val & 0xFF # WTM[7:0]

        regVal = self._i2c.readByte(self.address, self.kRegFifoCtrl2)

        regVal &= ~self.kFifoCtrl2MaskWtm
        regVal |= (ctrl2Val << self.kFifoCtrl2ShiftWtm)

        self._i2c.writeByte(self.address, self.kRegFifoCtrl2, regVal)

        self._i2c.writeByte(self.address, self.kRegFifoCtrl1, ctrl1Val)

    def set_fifo_mode(self, val):
        """
        Sets the FIFO mode

        :param val: The FIFO mode
        :type val: int

        Possible values:
            - kBypassMode
            - kFifoMode
            - kStreamToFifoMode
            - kBypassToStreamMode
            - kStreamMode
            - kBypassToFifoMode
        """
        if val < self.kBypassMode or val > self.kBypassToFifoMode:
            return
        
        regVal = self._i2c.readByte(self.address, self.kRegFifoCtrl4)

        regVal &= ~self.kFifoCtrl4MaskFifoMode
        regVal |= (val << self.kFifoCtrl4ShiftFifoMode)

        self._i2c.writeByte(self.address, self.kRegFifoCtrl4, regVal)

    def set_accel_fifo_batch_set(self, val):
        """
        Sets the batch data rate for the accelerometer

        :param val: The batch data rate
        :type val: int

        See the "Possible Accelerometer Batch Data Rates" in the class definition for a list of valid arguments
        """
        if val < self.kXlNotBatched or val > self.kXlBatchedAt6Hz5:
            return

        regVal = self._i2c.readByte(self.address, self.kRegFifoCtrl3)

        regVal &= ~self.kFifoCtrl3MaskBdrXl
        regVal |= (val << self.kFifoCtrl3ShiftBdrXl)
        
        self._i2c.writeByte(self.address, self.kRegFifoCtrl3, regVal)


    def set_gyro_fifo_batch_set(self, val):
        """
        Sets the batch data rate for the gyroscope

        :param val: The batch data rate
        :type val: int

        See the "Possible Gyroscope Batch Data Rates" in the class definition for a list of valid arguments
        """
        if val < self.kGyroNotBatched or val > self.kGyroBatchedAt6Hz5:
            return

        regVal = self._i2c.readByte(self.address, self.kRegFifoCtrl3)

        regVal &= ~self.kFifoCtrl3MaskBdrG
        regVal |= (val << self.kFifoCtrl3ShiftBdrG)
        
        self._i2c.writeByte(self.address, self.kRegFifoCtrl3, regVal)
    
    def set_fifo_timestamp_dec(self, val):
        """
        Sets the FIFO time stamp decimation rate.

        :param val: The decimation rate
        :type val: int

        Possible values:
            - kNoDecimation
            - kDec1
            - kDec8
            - kDec32
        """
        if val < self.kNoDecimation or val > self.kDec32:
            return
        
        regVal = self._i2c.readByte(self.address, self.kRegFifoCtrl4)

        regVal &= ~self.kFifoCtrl4MaskOdrTsBatch
        regVal |= (val << self.kFifoCtrl4ShiftOdrTsBatch)

        self._i2c.writeByte(self.address, self.kRegFifoCtrl4, regVal)

    # Interrupt and pin mode settings
    def set_pin_mode(self, activeLow):
        """
        Sets the active state of the interrupt pin - high or low.

        :param activeLow: Set to `True` for active low, `False` for active high
        :type activeLow: bool
        """
        if activeLow != True and activeLow != False:
            return

        regVal = self._i2c.readByte(self.address, self.kRegCtrl3C)

        regVal &= ~self.kCtrl3CMaskHlActive
        regVal |= (activeLow << self.kCtrl3CShiftHlActive)

        if activeLow:
            # pinmode must be set to push-pull when active low is set.
            # See section 9.14 on pg 51 of datasheet for more information
            regVal &= ~self.kCtrl3CMaskPpOd

        self._i2c.writeByte(self.address, self.kRegCtrl3C, regVal)

    def set_int_notification(self, val):
        """
        Sets what triggers an interrupt

        :param val: The interrupt event type
        :type val: int

        Possible Values:
            - kAllIntPulsed
            - kBaseLatchedEmbPulsed
            - kBasePulsedEmbLatched
            - kAllIntLatched
        """
        if val < self.kAllIntPulsed or val > self.kAllIntLatched:
            return


        lir = val & 0x01
        intClrOnRead = val & 0x01

        # Set necessary values in the tap config register
        regVal = self._i2c.readByte(self.address, self.kRegTapCfg0)

        regVal &= ~(self.kTapCfg0MaskLir | self.kTapCfg0MaskIntClrOnRead)
        regVal |= (lir << self.kTapCfg0ShiftLir)
        regVal |= (intClrOnRead << self.kTapCfg0ShiftIntClrOnRead)
        
        self._i2c.writeByte(self.address, self.kRegTapCfg0, regVal)

        # Set necessary values in the Page RW register
        self._mem_bank_set(self.kEmbeddedFuncBank)

        regVal = self._i2c.readByte(self.address, self.kRegPageRw)

        embFuncLir = (val & 0x02) >> 1
        regVal &= ~self.kPageRwMaskEmbFuncLir
        regVal |= (embFuncLir << self.kPageRwShiftEmbFuncLir)

        self._i2c.writeByte(self.address, self.kRegPageRw, regVal)

        self._mem_bank_set(self.kUserBank)

    class _PinIntRoute:
        """
        The routing information for an interrupt pin
        """
        def __init__(self):
            self.int_ctrl = 0
            self.md_cfg = 0
            self.emb_func_int = 0
            self.fsm_int_a = 0
            self.fsm_int_b = 0
            self.mlc_int = 0

    def _pin_int1_route_get(self):
        """
        Get the routing information from registers INT1_CTRL, MD1_CFG,
        EMB_FUNC_INT1, FSM_INT1_A, FSM_INT1_B

        :return: The routing information
        :rtype: PinIntRoute
        """
        route = self._PinIntRoute()

        self._mem_bank_set(self.kEmbeddedFuncBank)

        route.mlc_int = self._i2c.readByte(self.address, self.kRegMlcInt1)
        route.emb_func_int = self._i2c.readByte(self.address, self.kRegEmbFuncInt1)
        route.fsm_int_a = self._i2c.readByte(self.address, self.kRegFsmInt1A)
        route.fsm_int_b = self._i2c.readByte(self.address, self.kRegFsmInt1B)

        self._mem_bank_set(self.kUserBank)
        
        route.int_ctrl = self._i2c.readByte(self.address, self.kRegInt1Ctrl)
        route.md_cfg = self._i2c.readByte(self.address, self.kRegMd1Cfg)

        return route

    def _pin_int2_route_get(self):
        """
        Get the routing information from registers INT2_CTRL,  MD2_CFG,
        EMB_FUNC_INT2, FSM_INT2_A, FSM_INT2_B

        :return: The routing information
        :rtype: PinIntRoute
        """
        route = self._PinIntRoute()

        self._mem_bank_set(self.kEmbeddedFuncBank)

        route.mlc_int = self._i2c.readByte(self.address, self.kRegMlcInt2)
        route.emb_func_int = self._i2c.readByte(self.address, self.kRegEmbFuncInt2)
        route.fsm_int_a = self._i2c.readByte(self.address, self.kRegFsmInt2A)
        route.fsm_int_b = self._i2c.readByte(self.address, self.kRegFsmInt2B)

        self._mem_bank_set(self.kUserBank)
        
        route.int_ctrl = self._i2c.readByte(self.address, self.kRegInt2Ctrl)
        route.md_cfg = self._i2c.readByte(self.address, self.kRegMd2Cfg)

        return route
    
    def _pin_int1_route_set(self, val):
        """
        Set the routing information to registers INT1_CTRL, MD1_CFG,
        EMB_FUNC_INT1, FSM_INT1_A, FSM_INT1_B
        
        :param val: The routing information
        :type val: PinIntRoute
        """
        self._mem_bank_set(self.kEmbeddedFuncBank)

        self._i2c.writeByte(self.address, self.kRegMlcInt1, val.mlc_int)
        self._i2c.writeByte(self.address, self.kRegEmbFuncInt1, val.emb_func_int)
        self._i2c.writeByte(self.address, self.kRegFsmInt1A, val.fsm_int_a)
        self._i2c.writeByte(self.address, self.kRegFsmInt1B, val.fsm_int_b)

        self._mem_bank_set(self.kUserBank)

        embFunEn = (
            (val.emb_func_int & self.kEmbFuncInt1MaskFsmLc) or
            (val.emb_func_int & self.kEmbFuncInt1MaskSigMot) or
            (val.emb_func_int & self.kEmbFuncInt1MaskTilt) or
            (val.emb_func_int & self.kEmbFuncInt1MaskStepDetector)
        )

        if embFunEn or (val.fsm_int_a) or (val.fsm_int_b) or (val.mlc_int):
            val.md_cfg |= self.kMd1CfgMaskInt1EmbFunc
        else:
            val.md_cfg &= ~self.kMd1CfgMaskInt1EmbFunc
        
        self._i2c.writeByte(self.address, self.kRegInt1Ctrl, val.int_ctrl)
        self._i2c.writeByte(self.address, self.kRegMd1Cfg, val.md_cfg)

        tapCfg2 = self._i2c.readByte(self.address, self.kRegTapCfg2)

        intsEnable = (
            (val.md_cfg & self.kMd1CfgMaskInt1Shub) or
            (val.md_cfg & self.kMd1CfgMaskInt16d) or
            (val.md_cfg & self.kMd1CfgMaskInt1DoubleTap) or
            (val.md_cfg & self.kMd1CfgMaskInt1Ff) or
            (val.md_cfg & self.kMd1CfgMaskInt1Wu) or
            (val.md_cfg & self.kMd1CfgMaskInt1SingleTap) or
            (val.md_cfg & self.kMd1CfgMaskInt1SleepChange)
        )

        if intsEnable or val.int_ctrl:
            tapCfg2 |= self.kTapCfg2MaskInterruptsEnable
        else:
            tapCfg2 &= ~self.kTapCfg2MaskInterruptsEnable

        self._i2c.writeByte(self.address, self.kRegTapCfg2, tapCfg2)

    def _pin_int2_route_set(self, val):
        """
        Select the signal that needs to route on the int2 pad

        :param val: The routing information
        :type val: PinIntRoute
        """
        self._mem_bank_set(self.kEmbeddedFuncBank)

        self._i2c.writeByte(self.address, self.kRegMlcInt2, val.mlc_int)
        self._i2c.writeByte(self.address, self.kRegEmbFuncInt2, val.emb_func_int)
        self._i2c.writeByte(self.address, self.kRegFsmInt2A, val.fsm_int_a)
        self._i2c.writeByte(self.address, self.kRegFsmInt2B, val.fsm_int_b)

        self._mem_bank_set(self.kUserBank)

        embFunEn = (
            (val.emb_func_int & self.kEmbFuncInt2MaskFsmLc) or
            (val.emb_func_int & self.kEmbFuncInt2MaskSigMot) or
            (val.emb_func_int & self.kEmbFuncInt2MaskTilt) or
            (val.emb_func_int & self.kEmbFuncInt2MaskStepDetector)
        )

        if embFunEn or (val.fsm_int_a) or (val.fsm_int_b) or (val.mlc_int):
            val.md_cfg |= self.kMd2CfgMaskInt2EmbFunc
        else:
            val.md_cfg &= ~self.kMd2CfgMaskInt2EmbFunc
        
        self._i2c.writeByte(self.address, self.kRegInt2Ctrl, val.int_ctrl)
        self._i2c.writeByte(self.address, self.kRegMd2Cfg, val.md_cfg)

        tapCfg2 = self._i2c.readByte(self.address, self.kRegTapCfg2)

        intCtrlEn = (
            (val.int_ctrl & self.kInt2CtrlMaskInt2DrdyXl) or
            (val.int_ctrl & self.kInt2CtrlMaskInt2DrdyG) or
            (val.int_ctrl & self.kInt2CtrlMaskInt2DrdyTemp) or
            (val.int_ctrl & self.kInt2CtrlMaskInt2FifoTh) or
            (val.int_ctrl & self.kInt2CtrlMaskInt2FifoOvr) or
            (val.int_ctrl & self.kInt2CtrlMaskInt2FifoFull) or
            (val.int_ctrl & self.kInt2CtrlMaskInt2CntBdr)
        )

        md2CfgEn = (
            (val.md_cfg & self.kMd2CfgMaskInt26d) or
            (val.md_cfg & self.kMd2CfgMaskInt2DoubleTap) or
            (val.md_cfg & self.kMd2CfgMaskInt2Ff) or
            (val.md_cfg & self.kMd2CfgMaskInt2Wu) or
            (val.md_cfg & self.kMd2CfgMaskInt2SingleTap) or
            (val.md_cfg & self.kMd2CfgMaskInt2SleepChange)
        )

        if intCtrlEn or md2CfgEn:
            tapCfg2 |= self.kTapCfg2MaskInterruptsEnable
        else:
            tapCfg2 &= ~self.kTapCfg2MaskInterruptsEnable
        
        self._i2c.writeByte(self.address, self.kRegTapCfg2, tapCfg2)

        
    def set_accel_status_to_int1(self, enable):
        """
        Sends the accelerometer's data ready signal to interrupt one.

        :param enable: Enable or disable the accelerometer status to the interrupt pin
        :type enable: bool
        """
        if enable != True and enable != False:
            return

        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.kInt1CtrlMaskInt1DrdyXl
        route.int_ctrl |= (enable << self.kInt1CtrlShiftInt1DrdyXl)

        self._pin_int1_route_set(route)
    

    def set_fifo_threshold_int1(self, enable):
        """
        Sends the accelerometer's data ready signal to interrupt one.

        :param enable: Enable or disable the accelerometer status to the interrupt pin
        :type enable: bool
        """
        if enable != True and enable != False:
            return

        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.kInt1CtrlMaskInt1FifoTh
        route.int_ctrl |= (enable << self.kInt1CtrlShiftInt1FifoTh)

        self._pin_int1_route_set(route)

    def set_batch_counter_int1(self, enable):
        """
        Sends the accelerometer's data ready signal to interrupt one.

        :param enable: Enable or disable the accelerometer status to the interrupt pin
        :type enable: bool
        """
        if enable != True and enable != False:
            return

        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.kInt1CtrlMaskInt1CntBdr
        route.int_ctrl |= (enable << self.kInt1CtrlShiftInt1CntBdr)

        self._pin_int1_route_set(route)

    def set_accel_status_to_int2(self, enable):
        """
        Sends the accelerometer's data ready signal to interrupt two.
        
        :param enable: Enable or disable the accelerometer status to the interrupt pin
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        route = self._pin_int2_route_get()

        route.int_ctrl &= ~self.kInt2CtrlMaskInt2DrdyXl
        route.int_ctrl |= (enable << self.kInt2CtrlShiftInt2DrdyXl)

        self._pin_int2_route_set(route)
    
    def set_gyro_status_to_int1(self, enable):
        """
        Sends the gyroscope's data ready signal to interrupt one.
        
        :param enable: Enable or disable the gyroscope status to the interrupt pin
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        route = self._pin_int1_route_get()

        route.int_ctrl &= ~self.kInt1CtrlMaskInt1DrdyG
        route.int_ctrl |= (enable << self.kInt1CtrlShiftInt1DrdyG)

        self._pin_int1_route_set(route)

    def set_gyro_status_to_int2(self, enable):
        """
        Sends the gyroscope's data ready signal to interrupt two.
        
        :param enable: Enable or disable the gyroscope status to the interrupt pin
        :type enable: bool
        """
        if enable != True and enable != False:
            return
        
        route = self._pin_int2_route_get()

        route.int_ctrl &= ~self.kInt2CtrlMaskInt2DrdyG
        route.int_ctrl |= (enable << self.kInt2CtrlShiftInt2DrdyG)

        self._pin_int2_route_set(route)

    def set_data_ready_mode(self, val):
        """
        Sets how the data ready signal is latched i.e. only return zero after interface reading
        OR is pulsed.
        
        :param val: The data ready mode.
        :type val: int

        Possible values:
            - kDataReadyPulsed
            - kDataReadyLatched
        """
        if val < self.kDataReadyPulsed or val > self.kDataReadyLatched:
            return

        regVal = self._i2c.readByte(self.address, self.kRegCntrBdr1)

        regVal &= ~self.kCntrBdr1ShiftDatareadyPulsed
        regVal |= (val << self.kCntrBdr1ShiftDatareadyPulsed)

        self._i2c.writeByte(self.address, self.kRegCntrBdr1, regVal)
    
    def set_hub_odr(self, rate):
        """
        Sets the output data rate for the sensor hub.

        :param rate: The output data rate
        :type rate: int

        Possible values:
            - kShOdr104Hz
            - kShOdr52Hz
            - kShOdr26Hz
            - kShOdr13Hz
        """
        if rate < self.kShOdr104Hz or rate > self.kShOdr13Hz:
            return
        
        self._mem_bank_set(self.kSensorHubBank)

        regVal = self._i2c.readByte(self.address, self.kRegSlv0Config)

        regVal &= ~self.kSlv0ConfigMaskShubOdr
        regVal |= (rate << self.kSlv0ConfigShiftShubOdr)

        self._i2c.writeByte(self.address, self.kRegSlv0Config, regVal)

        self._mem_bank_set(self.kUserBank)
    
    class _SensorSettings():
        def __init__(self):
            self.address = 0
            self.subAddress = 0
            self.data = 0

    # TODO: Add more methods as needed
