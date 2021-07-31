do
--create an instance of the IADS
redIADS = SkynetIADS:create('russia')

---debug settings remove from here on if you do not wan't any output on what the IADS is doing by default
--local iadsDebug = redIADS:getDebugSettings()
--iadsDebug.IADSStatus = true
--iadsDebug.radarWentDark = true
--iadsDebug.contacts = true
--iadsDebug.radarWentLive = true
--iadsDebug.noWorkingCommmandCenter = false
--iadsDebug.ewRadarNoConnection = false
--iadsDebug.samNoConnection = false
--iadsDebug.jammerProbability = true
--iadsDebug.addedEWRadar = false
--iadsDebug.hasNoPower = false
--iadsDebug.harmDefence = true
--iadsDebug.samSiteStatusEnvOutput = true
--iadsDebug.earlyWarningRadarStatusEnvOutput = true
--iadsDebug.commandCenterStatusEnvOutput = true
---end remove debug ---

--add all units with unit name beginning with 'EW' to the IADS:
redIADS:addEarlyWarningRadarsByPrefix('EW')

--add all groups begining with group name 'SAM' to the IADS:
redIADS:addSAMSitesByPrefix('IADS')


--add a command center:
--commandCenter = StaticObject.getByName('Command-Center')
--redIADS:addCommandCenter(commandCenter)

---we add a K-50 AWACs, manually. This could just as well be automated by adding an 'EW' prefix to the unit name:
--redIADS:addEarlyWarningRadar('AWACS-K-50')

--add a power source and a connection node for this EW radar:
--local powerSource = StaticObject.getByName('Power-Source-EW-Center3')
--local connectionNodeEW = StaticObject.getByName('Connection-Node-EW-Center3')
--redIADS:getEarlyWarningRadarByUnitName('EW-Center3'):addPowerSource(powerSource):addConnectionNode(connectionNodeEW)

--add a connection node to this SA-2 site, and set the option for it to go dark, if it looses connection to the IADS:
--local connectionNode = Unit.getByName('Mobile-Command-Post-SAM-SA-2')
--redIADS:getSAMSitesByGroupName('SAM-SA-2'):addConnectionNode(connectionNode):setAutonomousBehaviour(SkynetIADSAbstractRadarElement.AUTONOMOUS_STATE_DARK)

--this SA-2 site will go live at 70% of its max search range:
redIADS:getSAMSitesByPrefix('IADS_LR'):setEngagementZone(SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_KILL_ZONE):setGoLiveRangeInPercent(30)
redIADS:getSAMSitesByPrefix('IADS_MR'):setEngagementZone(SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_KILL_ZONE):setGoLiveRangeInPercent(40)
redIADS:getSAMSitesByPrefix('IADS_SR'):setEngagementZone(SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_SEARCH_RANGE):setGoLiveRangeInPercent(70)
redIADS:getSAMSitesByPrefix('IADS_AAA'):setEngagementZone(SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_SEARCH_RANGE):setGoLiveRangeInPercent(80)
redIADS:getSAMSitesByPrefix('IADS_IR'):setEngagementZone(SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_SEARCH_RANGE):setGoLiveRangeInPercent(80)


--all SA-10 sites shall act as EW sites, meaning their radars will be on all the time:
--redIADS:getSAMSitesByNatoName('SA-10'):setActAsEW(true)

--set the sa15 as point defence for the SA-10 site, we set it to always react to a HARM so we can demonstrate the point defence mechanism in Skynet
local sa15_pd_ewnorth = redIADS:getSAMSiteByGroupName('IADS_SR SA-15 PD EW North')
redIADS:getEarlyWarningRadarByUnitName('EW2 EWR north'):addPointDefence(sa15_pd_ewnorth):setHARMDetectionChance(100):setIgnoreHARMSWhilePointDefencesHaveAmmo(true)

local sa15_pd_ewsouth = redIADS:getSAMSiteByGroupName('IADS_SR SA-15 PD EW south')
redIADS:getEarlyWarningRadarByUnitName('EW1 EWR55G6'):addPointDefence(sa15_pd_ewsouth):setHARMDetectionChance(100):setIgnoreHARMSWhilePointDefencesHaveAmmo(true)


--set this SA-11 site to go live 70% of max range of its missiles (default value: 100%), its HARM detection probability is set to 50% (default value: 70%)
--redIADS:getSAMSitesByGroupName('SAM-SA-11'):setGoLiveRangeInPercent(70):setHARMDetectionChance(50)

--this SA-6 site will always react to a HARM being fired at it:
--redIADS:getSAMSitesByGroupName('SAM-SA-6'):setHARMDetectionChance(100)

--set this SA-11 site to go live at maximunm search range (default is at maximung firing range):
--redIADS:getSAMSitesByGroupName('SAM-SA-11-2'):setEngagementZone(SkynetIADSAbstractRadarElement.GO_LIVE_WHEN_IN_SEARCH_RANGE)

--activate the radio menu to toggle IADS Status output
redIADS:addRadioMenu()

-- activate the IADS
redIADS:activate()	

--add the jammer
--local jammer = SkynetIADSJammer:create(Unit.getByName('jammer-emitter'), redIADS)
--jammer:masterArmOn()
--jammer:addRadioMenu()

---some special code to remove the jammer aircraft if player is not flying with it in formation, has nothing to do with the IADS:
--local hornet = Unit.getByName('Hornet SA-11-2 Attack')
--if hornet == nil then
--	Unit.getByName('jammer-emitter'):destroy()
--	jammer:removeRadioMenu()
--end
--end special code


end