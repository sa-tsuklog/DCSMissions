do
    local nmBubbleSize = trigger.misc.getUserFlag('62')
    local shrinkTimer = trigger.misc.getUserFlag('61')
    trigger.action.outText("ASF [0:0] (1st Half) CZ Radius: ".. nmBubbleSize.."nm TTS: "\\shrinkTimer, 1,false)
end