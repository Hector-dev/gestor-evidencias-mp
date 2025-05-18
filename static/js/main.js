// Scripts para el Sistema de Gestión de Evidencias

document.addEventListener('DOMContentLoaded', function() {
  // Fade-out para mensajes flash
  const alerts = document.querySelectorAll('.alert:not(.no-auto-dismiss)');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      if (alert) {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }
    }, 5000);
  });

  // Tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
  popoverTriggerList.map(function(popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
  });
  
  // Aplicar estilos a elementos de formulario
  styleFormElements();
  
  // Validación de formularios
  validateForms();
});

// Aplicar estilos a los elementos de formulario
function styleFormElements() {
  // Añadir clase form-control a inputs y selects
  document.querySelectorAll('input:not([type="checkbox"]):not([type="radio"]), select, textarea').forEach(function(element) {
    element.classList.add('form-control');
  });
  
  // Añadir clase form-select a selects
  document.querySelectorAll('select').forEach(function(element) {
    element.classList.add('form-select');
    element.classList.remove('form-control');
  });
  
  // Añadir clase form-check-input a checkboxes y radios
  document.querySelectorAll('input[type="checkbox"], input[type="radio"]').forEach(function(element) {
    element.classList.add('form-check-input');
  });
}

// Validación de formularios
function validateForms() {
  const forms = document.querySelectorAll('form.needs-validation');
  
  Array.from(forms).forEach(function(form) {
    form.addEventListener('submit', function(event) {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      
      form.classList.add('was-validated');
    }, false);
  });
}

// Función para confirmar eliminación
function confirmDelete(event, message) {
  if (!confirm(message || '¿Está seguro de que desea eliminar este elemento? Esta acción no se puede deshacer.')) {
    event.preventDefault();
    return false;
  }
  return true;
}

// Función para previsualizar imágenes antes de cargar
function previewImage(input, previewElement) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
      const preview = document.getElementById(previewElement);
      if (preview) {
        preview.src = e.target.result;
        preview.style.display = 'block';
      }
    }
    
    reader.readAsDataURL(input.files[0]);
  }
} 