# POC

With `futurist` when calling `waiters.wait_for_any()` blocks if future has
called `Condition.wait()`.

This POC want help to test and debug related things:
- gilectomy
- futurist
- eventlet

Further readings:
- https://bugs.launchpad.net/futurist/+bug/1848457
- https://review.opendev.org/689691
- https://github.com/larryhastings/gilectomy

## Gilectomy

To test CPython without the GIL we can use the
[gilectomy branch of python](https://github.com/larryhastings/gilectomy)
and observe if behaviour have some change between the standard CPython version
and the CPython without the GIL.

It can be useful to compile and execute the gilectomy under an isolated
environment like a docker container to avoid possible side effects on your
system.
