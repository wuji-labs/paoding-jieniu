"""HTTP-facing layer (framework-agnostic handlers).

Handlers are thin: validate input, call a service, serialize the result.
They contain no money math — every numeric field they emit is produced
upstream by the service/domain layers and passed through verbatim.
"""
