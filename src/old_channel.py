




    def enable(self):
        self.visa.write(':disp 1' % self._channel)
        return self.enabled()

    def disable(self):
        self.visa.write(':disp 0' % self._channel)
        return self.disabled()

    def enabled(self):
        return bool(int(self.visa.ask(':disp?')))

    def disabled(self):
        return bool(int(self.visa.ask(':disp?'))) ^ 1

    def get_offset_V(self):
        return float(self.visa.ask(':off?'))

    def set_offset_V(self, offset):
        assert -1000 <= offset <= 1000.
        self.visa.write(':off %.4e' % offset)
        return self.get_offset_V()

    def get_range_V(self):
        return self.visa.ask(':rang?')

    def set_range_V(self, range):
        assert 8e-3 <= range <= 800.
        self.visa.write(':rang %.4e' % range)
        return self.get_range_V()

    def set_vertical_scale_V(self, scale):
        assert 1e-3 <= scale <= 100
        self.visa.write(':scal %.4e' % scale)

    def get_probe_ratio(self):
        return float(self.visa.ask(':prob?'))

    def set_probe_ratio(self, ratio):
        assert ratio in (0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1,\
                         2, 5, 10, 20, 50, 100, 200, 500, 1000)
        self.visa.write(':prob %s' % ratio)
        return self.get_probe_ratio()

    def get_units(self):
        return self.visa.ask(':unit?')

    def set_units(self, unit):
        unit = unit.lower()
        assert unit in ('volt', 'watt', 'amp', 'unkn')
        self.visa.write(':unit %s' % unit)

        

    def get_data_premable(self):
        '''
        Get information about oscilloscope axes.

        Returns:
            dict: A dictionary containing general oscilloscope axes information.
        '''
        pre = self._osc.visa.ask(':wav:pre?').split(',')
        pre_dict = {
            'format': int(pre[0]),
            'type': int(pre[1]),
            'points': int(pre[2]),
            'count': int(pre[3]),
            'xincrement': float(pre[4]),
            'xorigin': float(pre[5]),
            'xreference': float(pre[6]),
            'yincrement': float(pre[7]),
            'yorigin': float(pre[8]),
            'yreference': float(pre[9]),
        }
        return pre_dict

    def get_data(self, mode='norm', filename=None):
        '''
        Download the captured voltage points from the oscilloscope.

        Args:
            mode (str): 'norm' if only the points on the screen should be
                downloaded, and 'raw' if all the points the ADC has captured
                should be downloaded.  Default is 'norm'.
            filename (None, str): Filename the data should be saved to.  Default
                is `None`; the data is not saved to a file.

        Returns:
            2-tuple: A tuple of two lists.  The first list is the time values
                and the second list is the voltage values.

        '''
        assert mode in ('norm', 'raw')

        # Setup scope
        self._osc.visa.write(f':stop')
        self._osc.visa.write(f':wav:sour chan{self._channel}')
        self._osc.visa.write(f':wav:mode {mode}')
        self._osc.visa.write(f':wav:form byte')

        info = self.get_data_premable()

        max_num_pts = 250000
        num_blocks = info['points'] // max_num_pts
        last_block_pts = info['points'] % max_num_pts

        datas = []
        for i in _tqdm.tqdm(range(num_blocks+1), ncols=60):
            if i < num_blocks:
                self._osc.visa.write(f':wav:star {(1+i*250000)}')
                self._osc.visa.write(f':wav:stop {(250000*(i+1))}')
            else:
                if last_block_pts:
                    self._osc.visa.write(f':wav:star {(1+num_blocks*250000)}')
                    self._osc.visa.write(f':wav:stop {(num_blocks*250000+last_block_pts)}')
                else:
                    break
            data = self._osc.visa.ask_raw(':wav:data?')[11:]
            data = _np.frombuffer(data, 'B')
            datas.append(data)

        datas = _np.concatenate(datas)
        v = (datas - info['yorigin'] - info['yreference']) * info['yincrement']

        t = _np.arange(0, info['points']*info['xincrement'], info['xincrement'])
        # info['xorigin'] + info['xreference']

        if filename:
            try:
                os.remove(filename)
            except OSError:
                pass
            _np.savetxt(filename, _np.c_[t, v], '%.12e', ',')

        return t, v
