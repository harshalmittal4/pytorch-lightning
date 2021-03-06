# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from apex import amp
except ImportError:
    amp = None


class ApexPlugin:

    def __init__(self, trainer):
        self.trainer = trainer

    def connect(self, model, optimizers):
        model, optimizers = model.configure_apex(amp, model, optimizers, self.trainer.amp_level)
        self.trainer.reinit_scheduler_properties(optimizers, self.trainer.lr_schedulers)
        return model, optimizers

    def training_step(self, fx, args):
        output = fx(args)
        return output
