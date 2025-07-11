from src.models.ImageProcessor import ImageProcessor

from src.models.methods.Eikwel import Eikwel
from src.models.methods.Bernsen import Bernsen
from src.models.methods.Niblack import Niblack
from src.models.methods.Sauvola import Sauvola
from src.models.methods.Global import Global
from src.models.methods.WolfJolion import WolfJolion
from src.models.methods.Bradley import Bradley

class Controller:
    def __init__(self, view):
        self.view: None = None
        self.image = None
        self.result = None

    def load_image(self, path):
        self.image = ImageProcessor.read_image(path, gray_scale=False)
        return self.image

    def apply_method(self, method_name, params):
        if self.image is None:
            return None

        img_copy = self.image.copy()

        if method_name == "Глобальный":
            binarizer = Global(thresh=params.get("thresh", 128))
        elif method_name == "Бернсена":
            binarizer = Bernsen(window_size=15, contrast_threshold=15)
        elif method_name == "Ниблэка":
            binarizer = Niblack(
                window_size=params.get("window", 15),
                k=params.get("k", 0.2))
        elif method_name == "Саувола":
            binarizer = Sauvola(
                window_size=params.get("window", 25),
                k=params.get("k", 0.2))
        elif method_name == "Кристиана":
            binarizer = WolfJolion(
                window_size=params.get("window", 50),
                k=params.get("k", 0.5))
        elif method_name == "Брэдли":
            binarizer = Bradley(t=0.15)
        elif method_name == "Эйквеля":
            binarizer = Eikwel(
                r_size=params["r_size"],
                R_size=params["R_size"],
                eps=params["eps"],
                count=0)
        elif method_name == "Оцу":
            binarizer = Global(thresh="otsu")

        else:
            return None

        self.result = binarizer.threshold(img_copy)
        return self.result

    def save_result(self, path):
        if self.result is not None:
            ImageProcessor.save_image(self.result, path)

    def validate_method_params(self, method_name, params) -> bool:
        try:
            if method_name == "Глобальный":
                return isinstance(params.get("thresh"), int)
            elif method_name in {"Ниблэка", "Саувола", "Кристиана"}:
                window_raw = params.get("window")
                k_raw = params.get("k")
                if not window_raw or not k_raw:
                    return False
                params["window"] = int(window_raw)
                params["k"] = float(k_raw)
                return True
            elif method_name == "Эйквеля":
                r_raw = params.get("r_size")
                R_raw = params.get("R_size")
                eps_raw = params.get("eps")
                if not r_raw or not R_raw or not eps_raw:
                    return False
                params["r_size"] = int(r_raw)
                params["R_size"] = int(R_raw)
                params["eps"] = float(eps_raw)
                return True

            else: return True

        except (ValueError, TypeError):
            return False

    def collect_params(self, method_name, ui_elements: dict) -> dict:
        if method_name == "Глобальный":
            return {"thresh": ui_elements["thresh_slider"].value()}
        elif method_name == "Эйквеля":
            return {
                "r_size": ui_elements["r_size_input"].text(),
                "R_size": ui_elements["R_size_input"].text(),
                "eps": ui_elements["eps_input"].text()
            }
        elif method_name in {"Ниблэка", "Саувола", "Кристиана"}:
            return {
                "window": ui_elements["window_input"].text(),
                "k": ui_elements["k_input"].text()
            }

        return {}




