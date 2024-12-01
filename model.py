from tensorflow import keras
from tf_explain.core.grad_cam import GradCAM
import numpy as np
from PIL import Image

# Load pre-trained model
model = keras.models.load_model('malaria_model.h5', compile=False)
METRICS = ['binary_accuracy', keras.metrics.Precision(name="precision"), keras.metrics.Recall(name="recall")]
model.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3), loss="binary_crossentropy", metrics=METRICS)


async def prediction(img:Image.Image):
    img_array = img.resize((224, 224))  # Resize to model input size
    img_array = np.array(img_array)/255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Make prediction
    score = model.predict(img_array)[0]
    if score<0.5:
        predicted_class = 0
    else:
        predicted_class = 1
    
    gradcam_img = await generate_gradcam(img_array, model)
    
    return (predicted_class, score[0], gradcam_img)

async def generate_gradcam(image, model):
    # Initialize the GradCAM explainer
    explainer = GradCAM()
    
    # Generate the GradCAM heatmap
    grid = explainer.explain((image, None), model, class_index=0)

    # Convert heatmap (grid) to image
    heatmap_img = Image.fromarray(np.uint8(grid * 255))  # Convert to [0, 255] range
    return heatmap_img
