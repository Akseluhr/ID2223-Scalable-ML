import gradio as gr
import hopsworks

project = hopsworks.login()

dataset_api = project.get_dataset_api()
dataset_api.download("Resources/images/df_btc_prediction.png", overwrite=True)
dataset_api.download("Resources/images/df_btc_recent.png", overwrite=True)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            gr.Label("Ten past days price predictions")
            input_img = gr.Image("df_btc_prediction.png", elem_id="latest-prediction")
        with gr.Column():
            gr.Label("Ten past days RMSE")
            input_img = gr.Image("df_btc_recent.png", elem_id="recent-predictions")

demo.launch()
