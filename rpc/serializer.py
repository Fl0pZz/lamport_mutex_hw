import io
import pickle


def serialize(msg):
    buff = io.BytesIO()
    pickle.dump(msg, buff)
    data = buff.getvalue()
    return len(data).to_bytes(4, 'big') + data


def deserialize(data):
    buff = io.BytesIO(data)
    return pickle.load(buff)
