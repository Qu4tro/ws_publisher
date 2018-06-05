# ws publisher

Broadcast from stdin to all connected websocket clients

`term1 > mkfifo FIFO`

`term1> tail -f FIFO | python ws_publisher.py`

`term2> echo "hello world" > FIFO`

`term3> ws ws://localhost:8000`
`term3< hello world`

`term4> ws ws://localhost:8000`
`term4< hello world`

`term2> echo "hello again" > FIFO`
`term3< hello again`
`term4< hello again`
