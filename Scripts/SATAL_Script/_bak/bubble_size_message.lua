do
    local nmBubbleSize = trigger.misc.getUserFlag('62')
    trigger.action.outText("Bubble shrinked to ".. nmBubbleSize.."[nm]", 10,false)
end