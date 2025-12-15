"""
Modelo de Programación Lineal usando PuLP.
Este módulo encapsula toda la lógica de resolución de problemas de PL.
"""

from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, LpStatus, value


class LPModel:
    """
    Clase para manejar la creación y resolución de problemas de Programación Lineal.
    Soporta hasta 15 variables de decisión y 12 restricciones.
    """
    
    def __init__(self):
        """Inicializa el modelo de PL."""
        self.problem = None
        self.variables = {}  # Diccionario para almacenar todas las variables
        self.num_variables = 0
        self.status = None
        self.objective_value = None
        
    def create_problem(self, sense, objective_coefficients, variable_names=None, integer_vars=None):
        """
        Crea el problema de PL con la función objetivo.
        
        Args:
            sense (str): 'Maximizar' o 'Minimizar'
            objective_coefficients (list): Lista de coeficientes para cada variable
            variable_names (list, optional): Lista de nombres personalizados para variables
            integer_vars (list, optional): Lista de booleanos indicando si la variable es entera
        """
        sense_map = {
            'Maximizar': LpMaximize,
            'Minimizar': LpMinimize
        }
        
        self.problem = LpProblem("Problema_PL", sense_map[sense])
        self.num_variables = len(objective_coefficients)
        
        # Crear variables de decisión dinámicamente (no negativas por defecto)
        for i in range(self.num_variables):
            # Usar nombre personalizado si está disponible
            if variable_names and i < len(variable_names):
                var_name = variable_names[i]
            else:
                var_name = f"x{i+1}"
            
            # Determinar si la variable es entera
            is_integer = integer_vars and i < len(integer_vars) and integer_vars[i]
            cat = 'Integer' if is_integer else 'Continuous'
            
            self.variables[var_name] = LpVariable(var_name, lowBound=0, cat=cat)
        
        # Definir función objetivo usando los nombres de variables actuales
        var_list = list(self.variables.values())
        objective = sum(objective_coefficients[i] * var_list[i] 
                       for i in range(self.num_variables))
        self.problem += objective, "Funcion_Objetivo"
        
    def add_constraint(self, coefficients, constraint_type, rhs, name):
        """
        Añade una restricción al problema.
        
        Args:
            coefficients (list): Lista de coeficientes para cada variable
            constraint_type (str): Tipo de restricción: '<=', '>=', '='
            rhs (float): Valor del lado derecho de la restricción
            name (str): Nombre de la restricción
        """
        # Construir lado izquierdo de la restricción usando las variables en orden
        var_list = list(self.variables.values())
        lhs = sum(coefficients[i] * var_list[i] 
                 for i in range(len(coefficients)))
        
        if constraint_type == '<=':
            self.problem += lhs <= rhs, name
        elif constraint_type == '>=':
            self.problem += lhs >= rhs, name
        elif constraint_type == '=':
            self.problem += lhs == rhs, name
            
    def solve(self):
        """
        Resuelve el problema de PL.
        
        Returns:
            dict: Diccionario con el estado, valor objetivo y valores de variables
        """
        if self.problem is None:
            return {
                'status': 'Error',
                'message': 'El problema no ha sido creado correctamente.'
            }
        
        # Resolver el problema
        self.problem.solve()
        
        # Obtener estado
        self.status = LpStatus[self.problem.status]
        
        # Preparar resultado
        result = {
            'status': self.status,
            'status_code': self.problem.status
        }
        
        # Si es óptimo, obtener valores
        if self.status == 'Optimal':
            result['objective_value'] = value(self.problem.objective)
            # Almacenar valores de todas las variables
            result['variable_values'] = {
                var_name: value(var) for var_name, var in self.variables.items()
            }
            result['message'] = self._format_optimal_solution(result)
        else:
            result['message'] = self._format_non_optimal_solution(self.status)
            
        return result
    
    def _format_optimal_solution(self, result):
        """
        Formatea el mensaje para una solución óptima.
        
        Args:
            result (dict): Diccionario con los resultados
            
        Returns:
            str: Mensaje formateado
        """
        message = "✓ Solución Óptima Encontrada\n\n"
        message += f"Valor de la Función Objetivo: {result['objective_value']:.4f}\n\n"
        message += "Valores de las Variables:\n"
        
        # Mostrar valores de todas las variables en el orden original
        for var_name in self.variables.keys():
            var_value = value(self.variables[var_name])
            message += f"  {var_name} = {var_value:.4f}\n"
        
        return message.strip()
    
    def _format_non_optimal_solution(self, status):
        """
        Formatea el mensaje para soluciones no óptimas.
        
        Args:
            status (str): Estado del problema
            
        Returns:
            str: Mensaje formateado
        """
        status_messages = {
            'Infeasible': '✗ El problema es Inviable (Infeasible)\n\nNo existe una solución que satisfaga todas las restricciones.',
            'Unbounded': '✗ El problema es No Acotado (Unbounded)\n\nLa función objetivo puede crecer infinitamente.',
            'Not Solved': '✗ El problema No fue Resuelto (Not Solved)\n\nOcurrió un error durante la resolución.',
            'Undefined': '✗ Estado Indefinido (Undefined)\n\nEl problema no tiene un estado válido.'
        }
        
        return status_messages.get(status, f'✗ Estado desconocido: {status}')
