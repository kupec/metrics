# Packet loss and bandwidth degradation

## Model overview

For networks using TCP protocols we can observe bandwidth, latency and packet
loss metrics. Lets try to make a simple model of waiting for retransmission.

When packets are lost TCP should retransmit a segment and it decreases a
transmit speed due to round-trip time when we pauses sending packets. In reality
it's more complicated due to TCP window. Hovewer, it is interesting to analyze
retransmit delays even in such simplified case.

Consider an example, we send a big file over TCP connection. We have a bandwidth
1000 Mbit/s and ping time 50ms (RTT). We send some data during 10ms and loss a
packet. We wait 50ms RTT to retransmit packet and continue sending file chunks.
For first 10ms we sent 0.01s * 1000 Mbit/s = 10 Mbit of data. For next 50ms we
sent anything. So for 60ms we sent 10 Mbit of data and the effective speed is 10
Mbit / 0.06s = 166 Mbit/s. Not so good situation and we see that a network
latency can significally delay a stream of data.

## Formula

Lets do a more accurate evaluation. We have a bandwidth `b` bit/s, a ping `p` s,
a `M` bytes file and `mtu = 1500` bytes. Let `a` be a packet loss percent. If `a=0.01` it means
that every 100th packet is lost. What a time `t_0` to transfer the file without packet
lossing?

```
t_0 = 8 * M / b
```

To determine a time `t_1` with packet lossing lets divide this time to several
chunks. Each chunk contains two events - transferring bytes at `b` speed and
lossing packet. How much these chunks?

```
chunks_count = a * total_packets_count = a * M / mtu
```

So, `t_1 = chunks_count * (T_b + T_p)`. Where `T_b` - time of first event
(transferring bytes), `T_p` - time of waiting for retransmit lost packet (RTT =
ping). Continue

```
T_b = counts_of_packets_before_loss * (8 * mtu / b) = (1/a) * 8 * mtu / b
T_p = p
=>
t_1 = a * M / mtu * (8 * mtu / (a*b) + p)
=>
t_1 / t_0 = 1 + a*b*p / (8*mtu)
=>
(t_1 - t_0) / t_0 = a*b*p / (8*mtu)
```

The time `t_1` is the time `t_0` increased by some `X` percents, where `X ~ a*b*p`.
Therefore this percents increases linearly with bandwidth, latency and packet
loss percent.

If `b = 1000 Mbit/s, p = 2ms, a = 0.01`, then `t_0` is increased by 16%. When
the ping is changed to only 4ms, `t_0` is increased by twice percent - 33%.

## Tables with examples

For clarity we would evaluate effective bandwidth to compare it with bandwidth
without packet loss. The effective bandwidth is `8 * M / t_1` vs `8 * M / t_0 == b`

This is not a real data. Only some simple calculation. In reality it is probably
worse.

#### Fast Ethernet, 100 Mbit/s
| Ping | Packet loss=0.1% | Packet loss=0.5% | Packet loss=1% | Packet loss=3% | Packet loss=10% |
| --- | --- | --- | --- | --- | --- |
| 1ms | 99.2 Mbit/s | 96.0 Mbit/s | 92.3 Mbit/s | 80.0 Mbit/s | 54.5 Mbit/s |
| 2ms | 98.4 Mbit/s | 92.3 Mbit/s | 85.7 Mbit/s | 66.7 Mbit/s | 37.5 Mbit/s |
| 4ms | 96.8 Mbit/s | 85.7 Mbit/s | 75.0 Mbit/s | 50.0 Mbit/s | 23.1 Mbit/s |
| 10ms | 92.3 Mbit/s | 70.6 Mbit/s | 54.5 Mbit/s | 28.6 Mbit/s | 10.7 Mbit/s |
| 20ms | 85.7 Mbit/s | 54.5 Mbit/s | 37.5 Mbit/s | 16.7 Mbit/s | 5.7 Mbit/s |
| 50ms | 70.6 Mbit/s | 32.4 Mbit/s | 19.4 Mbit/s | 7.4 Mbit/s | 2.3 Mbit/s |
| 100ms | 54.5 Mbit/s | 19.4 Mbit/s | 10.7 Mbit/s | 3.8 Mbit/s | 1.2 Mbit/s |
| 200ms | 37.5 Mbit/s | 10.7 Mbit/s | 5.7 Mbit/s | 2.0 Mbit/s | 0.6 Mbit/s |
| 500ms | 19.4 Mbit/s | 4.6 Mbit/s | 2.3 Mbit/s | 0.8 Mbit/s | 0.2 Mbit/s |

#### Gigabit Ethernet, 1000 Mbit/s
| Ping | Packet loss=0.1% | Packet loss=0.5% | Packet loss=1% | Packet loss=3% | Packet loss=10% |
| --- | --- | --- | --- | --- | --- |
| 1ms | 923.1 Mbit/s | 705.9 Mbit/s | 545.5 Mbit/s | 285.7 Mbit/s | 107.1 Mbit/s |
| 2ms | 857.1 Mbit/s | 545.5 Mbit/s | 375.0 Mbit/s | 166.7 Mbit/s | 56.6 Mbit/s |
| 4ms | 750.0 Mbit/s | 375.0 Mbit/s | 230.8 Mbit/s | 90.9 Mbit/s | 29.1 Mbit/s |
| 10ms | 545.5 Mbit/s | 193.5 Mbit/s | 107.1 Mbit/s | 38.5 Mbit/s | 11.9 Mbit/s |
| 20ms | 375.0 Mbit/s | 107.1 Mbit/s | 56.6 Mbit/s | 19.6 Mbit/s | 6.0 Mbit/s |
| 50ms | 193.5 Mbit/s | 45.8 Mbit/s | 23.4 Mbit/s | 7.9 Mbit/s | 2.4 Mbit/s |
| 100ms | 107.1 Mbit/s | 23.4 Mbit/s | 11.9 Mbit/s | 4.0 Mbit/s | 1.2 Mbit/s |
| 200ms | 56.6 Mbit/s | 11.9 Mbit/s | 6.0 Mbit/s | 2.0 Mbit/s | 0.6 Mbit/s |
| 500ms | 23.4 Mbit/s | 4.8 Mbit/s | 2.4 Mbit/s | 0.8 Mbit/s | 0.2 Mbit/s |

#### 3G download, 7.2 Mbit/s
| Ping | Packet loss=0.1% | Packet loss=0.5% | Packet loss=1% | Packet loss=3% | Packet loss=10% |
| --- | --- | --- | --- | --- | --- |
| 1ms | 7.2 Mbit/s | 7.2 Mbit/s | 7.2 Mbit/s | 7.1 Mbit/s | 6.8 Mbit/s |
| 2ms | 7.2 Mbit/s | 7.2 Mbit/s | 7.1 Mbit/s | 6.9 Mbit/s | 6.4 Mbit/s |
| 4ms | 7.2 Mbit/s | 7.1 Mbit/s | 7.0 Mbit/s | 6.7 Mbit/s | 5.8 Mbit/s |
| 10ms | 7.2 Mbit/s | 7.0 Mbit/s | 6.8 Mbit/s | 6.1 Mbit/s | 4.5 Mbit/s |
| 20ms | 7.1 Mbit/s | 6.8 Mbit/s | 6.4 Mbit/s | 5.3 Mbit/s | 3.3 Mbit/s |
| 50ms | 7.0 Mbit/s | 6.3 Mbit/s | 5.5 Mbit/s | 3.8 Mbit/s | 1.8 Mbit/s |
| 100ms | 6.8 Mbit/s | 5.5 Mbit/s | 4.5 Mbit/s | 2.6 Mbit/s | 1.0 Mbit/s |
| 200ms | 6.4 Mbit/s | 4.5 Mbit/s | 3.3 Mbit/s | 1.6 Mbit/s | 0.6 Mbit/s |
| 500ms | 5.5 Mbit/s | 2.9 Mbit/s | 1.8 Mbit/s | 0.7 Mbit/s | 0.2 Mbit/s |

#### 4G download, 150 Mbit/s
| Ping | Packet loss=0.1% | Packet loss=0.5% | Packet loss=1% | Packet loss=3% | Packet loss=10% |
| --- | --- | --- | --- | --- | --- |
| 1ms | 148.1 Mbit/s | 141.2 Mbit/s | 133.3 Mbit/s | 109.1 Mbit/s | 66.7 Mbit/s |
| 2ms | 146.3 Mbit/s | 133.3 Mbit/s | 120.0 Mbit/s | 85.7 Mbit/s | 42.9 Mbit/s |
| 4ms | 142.9 Mbit/s | 120.0 Mbit/s | 100.0 Mbit/s | 60.0 Mbit/s | 25.0 Mbit/s |
| 10ms | 133.3 Mbit/s | 92.3 Mbit/s | 66.7 Mbit/s | 31.6 Mbit/s | 11.1 Mbit/s |
| 20ms | 120.0 Mbit/s | 66.7 Mbit/s | 42.9 Mbit/s | 17.6 Mbit/s | 5.8 Mbit/s |
| 50ms | 92.3 Mbit/s | 36.4 Mbit/s | 20.7 Mbit/s | 7.6 Mbit/s | 2.4 Mbit/s |
| 100ms | 66.7 Mbit/s | 20.7 Mbit/s | 11.1 Mbit/s | 3.9 Mbit/s | 1.2 Mbit/s |
| 200ms | 42.9 Mbit/s | 11.1 Mbit/s | 5.8 Mbit/s | 2.0 Mbit/s | 0.6 Mbit/s |
| 500ms | 20.7 Mbit/s | 4.7 Mbit/s | 2.4 Mbit/s | 0.8 Mbit/s | 0.2 Mbit/s |

