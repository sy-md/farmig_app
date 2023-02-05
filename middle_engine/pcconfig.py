import pynecone as pc


config = pc.Config(
    app_name="database_play",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
