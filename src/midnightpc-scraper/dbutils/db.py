import sqlite3

class Database:
    def __init__(self):
        self.DB_PATH = "test_db.sqlite"
        pass

    def init_tables(self):
        self._init_cpu_table()
    
    def add_rows(self, table, values):
        cursor = self.conn.cursor()
        cursor.executemany(
            f'''
            INSERT INTO {table} VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',
            values
        )
        self.conn.commit()

    def _init_cpu_table(self):
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cpu_properties = {

        }
        cursor = self.conn.cursor()
        cursor.execute(
            f'''
            CREATE TABLE IF NOT EXISTS cpu (
                name_display TEXT,
                name_brand TEXT,
                name_series TEXT,
                name_generation INT,
                name_sku INT,
                name_prefix TEXT,
                name_suffix TEXT,
                name_codename TEXT,
                architecture TEXT,
                msrp INT,
                launch_date TEXT,
                socket TEXT,
                n_cores_total INT,
                intel_n_cores_perf INT,
                intel_n_cores_eff INT,
                n_threads INT,
                max_turbo_freq REAL,
                base_freq REAL,
                intel_thermal_velocity_boost_freq REAL,
                intel_turbo_boost_max30_freq REAL,
                intel_perf_max_turbo_freq REAL,
                intel_eff_max_turbo_freq REAL,
                intel_perf_base_freq REAL,
                intel_eff_base_freq REAL,
                intel_smart_cache_total INT,
                cache_l1 INT,
                cache_l2 INT,
                cache_l3 INT,
                tdp_base INT,
                tdp_max INT,
                tjunc_temp INT,
                overclocking BOOL,
                memory_max INT,
                memory_types TEXT,
                memory_channels INT,
                memory_bandwith REAL,
                ecc_support BOOL,
                igpu_name_display TEXT,
                igpu_base_freq REAL,
                igpu_max_freq REAL,
                igpu_capabilities TEXT,
                igpu_cores INT,
                igpu_max_resolution_hdmi TEXT,
                igpu_max_resolution_dp TEXT,
                igpu_max_resolution_edp TEXT,
                igpu_directx REAL,
                igpu_opengl REAL,
                igpu_opencl REAL,
                igpu_n_codec_engines INT,
                igpu_max_displays INT,
                dmi_version REAL,
                dmi_lanes INT,
                pcie_version TEXT,
                pcie_config TEXT,
                pcie_max INT
            )
            '''
        )


if __name__ == "__main__":
    db = Database()
    db.init_tables()