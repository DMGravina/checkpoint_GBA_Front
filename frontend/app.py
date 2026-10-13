
import gradio as gr
import pandas as pd
from providers import api_provider

def update_leitura(tag):
    leitura = api_provider.leitura_atual(tag)
    if leitura:
        return f"Tensão: {leitura.get('tensao_v')} V\nCorrente: {leitura.get('corrente_a')} A\nTemperatura: {leitura.get('temp_c')} °C\nVibração: {leitura.get('vibracao_mms')} mm/s\nRotação: {leitura.get('rotacao_rpm')} RPM\nSeveridade Temperatura: {leitura.get('severidade_temp')}\nSeveridade Vibração: {leitura.get('severidade_vibracao')}"
    return "Falha ao obter leitura"

def update_historico(tag):
    historico = api_provider.historico_simulado(tag)
    if historico:
       df = pd.DataFrame(historico)
       return df
    return pd.DataFrame()
    
def update_observabilidade():
    obs = api_provider.get_observabilidade()
    if obs:
       df = pd.DataFrame(obs)
       return df
    return pd.DataFrame()

with gr.Blocks(title="Forzy Digital Twin - Sensores") as demo:
    gr.Markdown("# 📡 Monitoramento de Sensores")
    
    with gr.Row():
        tag_input = gr.Textbox(label="TAG do Equipamento (ex: MTR-001)", value="MTR-001")
        
    with gr.Tab("Leitura Atual"):
        btn_leitura = gr.Button("Atualizar Leitura")
        txt_leitura = gr.Textbox(label="Leitura Atual", lines=8)
        btn_leitura.click(fn=update_leitura, inputs=tag_input, outputs=txt_leitura)
        
    with gr.Tab("Histórico"):
        btn_historico = gr.Button("Atualizar Histórico")
        df_historico = gr.Dataframe(label="Histórico de Leituras")
        btn_historico.click(fn=update_historico, inputs=tag_input, outputs=df_historico)
        
    with gr.Tab("Observabilidade"):
        btn_obs = gr.Button("Atualizar Registros")
        df_obs = gr.Dataframe(label="Registros de Observabilidade")
        btn_obs.click(fn=update_observabilidade, inputs=None, outputs=df_obs)

if __name__ == "__main__":
    demo.launch()
