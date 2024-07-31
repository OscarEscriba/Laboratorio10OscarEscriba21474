def VertexShader (vertex, **kwargs): 
  modelMatrix = kwargs["modelMatrix"]
  #la camara estara aqui en vertexshader

  viewMatrix = kwargs["viewMatrix"]
  projectionMatrix = kwargs["projectionMatrix"]
  viewportMatrix = kwargs["viewportMatrix"]

  vt = [vertex[0],
        vertex[1],
        vertex[2],
        1]  #convertir el vertice en un tamaño de 4
  
  vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt 

  vt = vt.tolist()[0] 

  vt = [vt[0]/vt[3],
        vt[1]/vt[3],
        vt[2]/vt[3],
        vt[3]/vt[3]]
  
  return vt