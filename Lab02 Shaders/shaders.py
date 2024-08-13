#si voy a usar numpy aqui
import numpy as np


def vertexShader(vertex, **kwargs):
    # Se lleva a cabo por cada vertice
    
    # Recibimos las matrices
    modelMatrix = kwargs["modelMatrix"]
    viewMatrix = kwargs["viewMatrix"]
    projectionMatrix = kwargs["projectionMatrix"]
    viewportMatrix = kwargs["viewportMatrix"]
    
    # Agregamos un componente W al vertice
    vt = [vertex[0],
          vertex[1],
          vertex[2],
          1]
    
    # Transformamos el vertices por todas las matrices en el orden correcto
    vt = viewportMatrix * projectionMatrix * viewMatrix * modelMatrix @ vt
    
    vt = vt.tolist()[0]
    
    # Dividimos x,y,z por w para regresar el vertices a un tama�o de 3
    vt = [vt[0] / vt[3],
          vt[1] / vt[3],
          vt[2] / vt[3]]
    
    return vt


def fragmentShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4ta 5ta posicion del indice
    #los obtenemos y guardamos
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]


    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1
    
    vtP = [u*vtA[0] + v*vtB[0] + w*vtC[0],
           u*vtA[1] + v*vtB[1] + w*vtC[1]]
    
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    # Se regresa el color
    return [r,g,b]



def gouradShader(**kwargs):
    # Se lleva a cabo por cada pixel individual
    
    # Obtenemos la informacion requerida
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    #sabiendo que las coordenadas de textura estan en 4ta 5ta posicion del indice
    #los obtenemos y guardamos
    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    #sabiendo que los valores de las normales 
    #estan en la 6ta 7ta 8va posicion hacemos lo mismo
    #asumismo que vienen normalizadas
    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    #normal de este pixel
    normal = [u*nA[0] + v*nB[0] + w*nC[0],
              u*nA[1] + v*nB[1] + w*nC[1],
              u*nA[2] + v*nB[2] + w*nC[2]]
    
  
    # Empezamos siempre con color blanco
    r = 1
    g = 1
    b = 1
    
    vtP = [u*vtA[0] + v*vtB[0] + w*vtC[0],
           u*vtA[1] + v*vtB[1] + w*vtC[1]]
    
    
    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]
    # Se regresa el color

    #la formula de iluminacion que va a ser para calcular la intensidad
    #de que tan iluminada esta la superficie
    #intesity = normal DOT -dirlight

    #implementacion de producto punto de dos vectores

    intesity = np.dot(normal, -np.array(dirLight))
    intesity = max(0, intesity)
    r*= intesity
    g*= intesity
    b*= intesity
    return [r,g,b]

def flatShader(**kwargs):
	
	A, B, C = kwargs["verts"]
	u, v, w = kwargs["bCoords"]
	texture = kwargs["texture"]
	dirLight = kwargs["dirLight"]

	vtA = [A[3], A[4]]
	vtB = [B[3], B[4]]
	vtC = [C[3], C[4]]
	
	nA = [A[5], A[6], A[7]]
	nB = [B[5], B[6], B[7]]
	nC = [C[5], C[6], C[7]]
	
	normal = [  (nA[0] + nB[0] + nC[0]) / 3,
				(nA[1] + nB[1] + nC[1]) / 3,
				(nA[2] + nB[2] + nC[2]) / 3]



	
	r = 1
	g = 1
	b = 1

	vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
			u * vtA[1] + v * vtB[1] + w * vtC[1] ]
	
	if texture:
		texColor = texture.getColor(vtP[0], vtP[1])
		
		r *= texColor[0]
		g *= texColor[1]
		b *= texColor[2]
		
	# intensity = normal DOT -dirlight
	intensity = np.dot(normal, -np.array(dirLight) )
	intensity = max(0, intensity)
	r *= intensity
	g *= intensity
	b *= intensity
	
	# Se regresa el color
	return [r,g,b]

def glowShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]
    camMatrix = kwargs["camMatrix"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
            u * nA[1] + v * nB[1] + w * nC[1],
            u * nA[2] + v * nB[2] + w * nC[2] ]

    r = 1
    g = 1
    b = 1

    vtP = [ u * vtA[0] + v * vtB[0] + w * vtC[0],
        u * vtA[1] + v * vtB[1] + w * vtC[1] ]

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])

    r *= texColor[0]
    g *= texColor[1]
    b *= texColor[2]

    # intensity = normal DOT -dirlight
    intensity = producto_punto(normal, negative_vector(dirLight) )
    intensity = max(0, intensity)
    r *= intensity
    g *= intensity
    b *= intensity 
    #GLOW
    yellow = [1,1,0]
    
    #eje z de la camara
    camForward = [camMatrix[0][2],
                  camMatrix[1][2],
                  camMatrix[2][2]]

    glowintensity =producto_punto(normal, camForward)
    glowintensity = max(0, glowintensity)
    r += yellow[0] * glowintensity
    g += yellow[1] * glowintensity
    b += yellow[2] * glowintensity
    # Se regresa el color
    return [
        min(1, r),
        min(1,g),
        min(1,b)]

def toonShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    dirLight = kwargs["dirLight"]

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    nA = [A[5], A[6], A[7]]
    nB = [B[5], B[6], B[7]]
    nC = [C[5], C[6], C[7]]

    normal = [u * nA[0] + v * nB[0] + w * nC[0],
              u * nA[1] + v * nB[1] + w * nC[1],
              u * nA[2] + v * nB[2] + w * nC[2]]

    r, g, b = 1, 1, 1

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    intensity = np.dot(normal, -np.array(dirLight))
    intensity = max(0, intensity)

    # Aplicamos pasos discretos para simular el efecto toon
    steps = 4
    intensity = (int(intensity * steps)) / steps

    r *= intensity
    g *= intensity
    b *= intensity

    return [r, g, b]

def waterShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    time = kwargs["time", 0]  # Tiempo actual

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Modificación ondulante
    waveFactor = 0.1 * np.sin(10 * vtP[0] + time) + 0.1 * np.cos(10 * vtP[1] + time)
    vtP[0] += waveFactor
    vtP[1] += waveFactor

    r, g, b = 0.0, 0.4, 1.0  # Azul agua

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    return [r, g, b]

def fireShader(**kwargs):
    A, B, C = kwargs["verts"]
    u, v, w = kwargs["bCoords"]
    texture = kwargs["texture"]
    time = kwargs["time"]  # Tiempo actual

    vtA = [A[3], A[4]]
    vtB = [B[3], B[4]]
    vtC = [C[3], C[4]]

    vtP = [u * vtA[0] + v * vtB[0] + w * vtC[0],
           u * vtA[1] + v * vtB[1] + w * vtC[1]]

    # Desplazamiento dinámico para simular movimiento del fuego
    fireFactor = 0.1 * np.sin(5 * vtP[0] + time) + 0.2 * np.cos(5 * vtP[1] - time)
    vtP[1] += fireFactor

    r, g, b = 1.0, 0.5, 0.0  # Color fuego base

    if texture:
        texColor = texture.getColor(vtP[0], vtP[1])
        r *= texColor[0]
        g *= texColor[1]
        b *= texColor[2]

    # Añadimos un gradiente de color dinámico
    gradFactor = max(0, np.sin(vtP[1] + time))
    r += gradFactor * 0.5
    g += gradFactor * 0.3
    b += gradFactor * 0.1

    return [min(1, r), min(1, g), min(1, b)]

def basicLightingShader(**kwargs):
    # Obtén las normales, coordenadas de textura y textura activa
    bCoords = kwargs["bCoords"]
    texture = kwargs.get("texture")
    normal = kwargs["verts"][2]  # Normal del vértice

    # Luz direccional básica
    lightDir = [0, 0, -1]  # Luz que viene de frente
    intensity = max(0, sum(n * l for n, l in zip(normal, lightDir)))

    # Color base de la textura o un color fijo si no hay textura
    if texture:
        texColor = texture.getColor(*bCoords)
    else:
        texColor = [1, 1, 1]  # Color blanco por defecto

    # Aplica la iluminación
    shadedColor = [c * intensity for c in texColor]
    return shadedColor

def gradientLambertShader(**kwargs):
    # Información de entrada
    bCoords = kwargs["bCoords"]
    normal = kwargs["verts"][2]  # Normal del vértice
    position = kwargs["verts"][0]  # Posición del vértice en el espacio
    texture = kwargs.get("texture")

    # Luz direccional básica
    lightDir = [0, 1, -1]  # Luz que viene desde arriba y al frente
    lightDirNorm = [l / (sum([x**2 for x in lightDir])**0.5) for l in lightDir]  # Normaliza la dirección

    # Intensidad de la luz difusa
    intensity = max(0, sum(n * l for n, l in zip(normal, lightDirNorm)))

    # Crea un degradado basado en la posición y la intensidad
    gradient = (position[1] + 1) / 2  # Escala y convierte el rango [-1, 1] -> [0, 1]

    # Color base
    baseColor = [gradient, 0.5 * gradient, 1 - gradient]  # Degradado azul-morado

    # Si hay textura, úsala como base
    if texture:
        texColor = texture.getColor(*bCoords)
        color = [c * intensity * t for c, t in zip(baseColor, texColor)]
    else:
        color = [c * intensity for c in baseColor]

    return color

