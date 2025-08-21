import gspread
import json
import os
from typing import List, Dict, Any, Optional

# --- INICIO DE CÓDIGO REESCRITO ---

class SheetsHandler:
    """
    Clase para manejar la conexión y las operaciones con Google Sheets.
    Gestiona la autenticación y proporciona métodos para leer y escribir datos.
    """

    def __init__(self, config_path: str = 'config.json'):
        """
        Inicializa el manejador de Google Sheets.

        Args:
            config_path (str): Ruta al archivo de configuración JSON.
        """
        self.gc: Optional[gspread.Client] = None
        self.config: Optional[Dict[str, Any]] = self._load_config(config_path)
        
        if self.config:
            self.authenticate()

    def _load_config(self, path: str) -> Optional[Dict[str, Any]]:
        """
        Carga el archivo de configuración JSON.

        Args:
            path (str): Ruta al archivo de configuración.

        Returns:
            Optional[Dict[str, Any]]: Un diccionario con la configuración o None si hay un error.
        """
        if not os.path.exists(path):
            print(f"Error: No se encuentra el archivo de configuración '{path}'.")
            return None
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: El archivo de configuración '{path}' no es un JSON válido: {e}")
            return None

    def authenticate(self) -> None:
        """
        Autentica con la API de Google usando el archivo de credenciales especificado
        en la configuración.
        """
        if not self.config:
            print("Error: No se puede autenticar sin una configuración válida.")
            return

        credentials_file = self.config.get('google_credentials_path')
        if not credentials_file or not os.path.exists(credentials_file):
            print(f"Error: No se encuentra el archivo de credenciales en la ruta: '{credentials_file}'.")
            return
            
        try:
            self.gc = gspread.service_account(filename=credentials_file)
            print("Autenticación con Google exitosa.")
        except gspread.exceptions.GSpreadException as e:
            print(f"Error durante la autenticación con la API de Google: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la autenticación: {e}")

    def _get_worksheet(self, sheet_url: str) -> Optional[gspread.Worksheet]:
        """
        Función auxiliar para abrir una hoja de cálculo y devolver la primera página (worksheet).

        Args:
            sheet_url (str): La URL de la hoja de cálculo.

        Returns:
            Optional[gspread.Worksheet]: El objeto de la primera página o None si hay un error.
        """
        if not self.gc:
            print("Error: Cliente de Google no autenticado.")
            return None
        try:
            sheet = self.gc.open_by_url(sheet_url)
            return sheet.sheet1
        except gspread.exceptions.SpreadsheetNotFound:
            print(f"Error: No se encontró la hoja de cálculo en la URL: {sheet_url}")
            return None
        except gspread.exceptions.GSpreadException as e:
            print(f"Error de gspread al acceder a la hoja {sheet_url}: {e}")
            return None

    def get_sheet_records(self, sheet_url: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de una hoja de cálculo como una lista de diccionarios.

        Args:
            sheet_url (str): La URL de la hoja de cálculo.

        Returns:
            List[Dict[str, Any]]: Lista de registros. Devuelve una lista vacía si hay un error.
        """
        worksheet = self._get_worksheet(sheet_url)
        if not worksheet:
            return []
        try:
            return worksheet.get_all_records()
        except gspread.exceptions.GSpreadException as e:
            print(f"Error al leer los registros de la hoja {sheet_url}: {e}")
            return []

    def get_sheet_headers(self, sheet_url: str) -> List[str]:
        """
        Lee únicamente la primera fila (encabezados) de una hoja de cálculo.
        
        Args:
            sheet_url (str): La URL de la hoja de cálculo.
            
        Returns:
            List[str]: Lista de encabezados. Devuelve una lista vacía si hay un error.
        """
        worksheet = self._get_worksheet(sheet_url)
        if not worksheet:
            return []
        try:
            return worksheet.row_values(1)
        except gspread.exceptions.GSpreadException as e:
            print(f"Error al leer los encabezados de la hoja {sheet_url}: {e}")
            return []

    def update_record(self, sheet_url: str, identifier_column: str, identifier_value: Any, 
                      column_to_update: str, new_value: Any) -> bool:
        """
        Actualiza una celda específica en una hoja de cálculo.

        Busca una fila por un valor único en una columna identificadora y actualiza
        otra celda en esa misma fila.

        Args:
            sheet_url (str): La URL de la hoja a modificar.
            identifier_column (str): El nombre de la columna para encontrar la fila (ej. 'numero_proceso').
            identifier_value (Any): El valor único para identificar la fila (ej. 'SIP-046-2025').
            column_to_update (str): El nombre de la columna a actualizar (ej. 'objeto_proceso').
            new_value (Any): El nuevo valor para la celda.

        Returns:
            bool: True si la actualización fue exitosa, False en caso contrario.
        """
        worksheet = self._get_worksheet(sheet_url)
        if not worksheet:
            return False
            
        try:
            # Paso 1: Encontrar la celda que identifica la fila.
            # Se busca el valor en la columna especificada.
            header_cell = worksheet.find(identifier_column)
            if not header_cell:
                print(f"Error de actualización: No se encontró la columna identificadora '{identifier_column}'")
                return False

            cell_to_find = worksheet.find(str(identifier_value), in_column=header_cell.col)
            if not cell_to_find:
                print(f"Error de actualización: No se encontró la fila con {identifier_column} = {identifier_value}")
                return False
            
            row_index = cell_to_find.row
            
            # Paso 2: Encontrar la columna que se va a actualizar.
            headers = worksheet.row_values(1)
            if column_to_update not in headers:
                print(f"Error de actualización: No se encontró la columna a actualizar '{column_to_update}'")
                return False
                
            col_index_to_update = headers.index(column_to_update) + 1
            
            # Paso 3: Actualizar la celda.
            worksheet.update_cell(row_index, col_index_to_update, new_value)
            print(f"Éxito: Se actualizó '{column_to_update}' a '{new_value}' en la fila identificada por '{identifier_value}'.")
            return True
            
        except gspread.exceptions.GSpreadException as e:
            print(f"Error de gspread al actualizar la hoja: {e}")
            return False
        except Exception as e:
            print(f"Ocurrió un error inesperado durante la actualización: {e}")
            return False

    def get_all_process_numbers(self) -> List[str]:
        """Obtiene todos los valores de la primera columna (excluyendo el encabezado) de la hoja de procesos."""
        sheet_url = self.config.get('procesos_sheet_url')
        worksheet = self._get_worksheet(sheet_url)
        if not worksheet:
            return []
        try:
            print("Leyendo números de proceso para validación.")
            return worksheet.col_values(1)[1:]
        except gspread.exceptions.GSpreadException as e:
            print(f"Error al leer los números de proceso: {e}")
            return []

    def deactivate_all_processes(self) -> bool:
        """Busca todas las celdas con "SI" en la columna 10 y las cambia a "NO"."""
        sheet_url = self.config.get('procesos_sheet_url')
        worksheet = self._get_worksheet(sheet_url)
        if not worksheet:
            return False
        try:
            # Es más seguro encontrar el índice de la columna por su nombre si es posible.
            # Por ahora, se mantiene la lógica original con la columna 10.
            active_cells = worksheet.findall("SI", in_column=10)
            for cell in active_cells:
                worksheet.update_cell(cell.row, cell.col, "NO")
            print(f"Se desactivaron {len(active_cells)} procesos anteriores.")
            return True
        except gspread.exceptions.GSpreadException as e:
            print(f"Error al desactivar procesos: {e}")
            return False

    def add_new_process(self, process_data_list: List[Any]) -> bool:
        """
        Añade una nueva fila con datos a la hoja de procesos.

        Args:
            process_data_list (List[Any]): Una lista de valores que representan la nueva fila.

        Returns:
            bool: True si la operación fue exitosa, False en caso contrario.
        """
        sheet_url = self.config.get('procesos_sheet_url')
        worksheet = self._get_worksheet(sheet_url)
        if not worksheet:
            return False
        try:
            worksheet.append_row(process_data_list, value_input_option='USER_ENTERED')
            print("Nuevo proceso añadido a la hoja de cálculo.")
            return True
        except gspread.exceptions.GSpreadException as e:
            print(f"Error al añadir el nuevo proceso: {e}")
            return False

# --- FIN DE CÓDIGO REESCRITO ---