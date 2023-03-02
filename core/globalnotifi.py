from Documents.models import Documentos

def valnotificacion():
    return len(Documentos.objects.filter(estado='No revisado'))