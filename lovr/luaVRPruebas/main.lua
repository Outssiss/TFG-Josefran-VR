texture = lovr.graphics.newTexture("camera_der_dist.png", {type = "2d", usage = {render}, label = "nose"})

function lovr.draw(pass)
    pass:draw(texture)
end