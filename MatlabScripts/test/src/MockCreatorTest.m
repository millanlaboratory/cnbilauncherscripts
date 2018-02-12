classdef MockCreatorTest < matlab.mock.TestCase & handle
    %MOCKCREATOR Summary of this class goes here
    %   Detailed explanation goes here
    
    properties
        mockCreator
    end
    
    methods(TestMethodSetup)
        function createController(testCase)
            import matlab.mock.constraints.WasCalled;
            import matlab.unittest.constraints.IsAnything;
            testCase.mockCreator =  MockCreator();
        end
    end
    
    methods (TestClassSetup)
        function setupPath(testCase)
            addpath([pwd '/../../src/']);
            testCase.addTeardown(@rmpath,[pwd '/../../src/']);
        end
    end
    
    methods (Test)
        function testMockCreator(testCase)
            testCase.verifyEqual(testCase.mockCreator.folder,'');
            testCase.verifyEqual(testCase.mockCreator.filename,'');
            testCase.verifyEqual(testCase.mockCreator.recursive, false);
        end
        
        function testExtractClassNameFromString(testCase)
            className = testCase.mockCreator.extractClassNameFromString(...
                'classdef MockCreatorTest < matlab.mock.TestCase & handle');
            testCase.verifyEqual(className, 'MockCreatorTest');
        end
        
        function testExtractClassNameFromEmptyString(testCase)
            className = testCase.mockCreator.extractClassNameFromString(...
                'MockCreatorTest < matlab.mock.TestCase & handle');
            testCase.verifyEqual(className, '');
        end
        
        function testExtractMethodsFromClassName(testCase)
            className = 'MockCreator';
            meth = methods(className);
            obtainedMethods = testCase.mockCreator.extractMethodsFromClassName(className);
            testCase.verifyEqual(obtainedMethods, [meth]);
        end
        
        function testExtractPropertiesFromClassName(testCase)
            className = 'MockCreator';
            prop1 = properties(className);
            prop2 = properties(superclasses('MockCreator'));
            obtainedProperties = testCase.mockCreator.extractPropertiesFromClassName(className);
            testCase.verifyEqual(obtainedProperties, [prop1; prop2]);
        end
        
        function testGenerateMockFileFromClassName(testCase)
            className = 'BCIController';
            success = false;
            addpath('/home/cnbi/dev/CritStabTaskBCI/src/');
            testCase.mockCreator.createMockFileFromClassName(className);
            try
                testCase.verifyEqual(exist('BCIControllerMock.m','file'), 2);
                testCase.verifyEqual(exist('BCIControllerMock','class'), 8);
                testCase.verifyEqual(properties('BCIControllerMock'),{'stub'; 'behavior'});
                testCase.verifyEqual(methods('BCIControllerMock'),{'BCIControllerMock'});
                bciControllerMock = BCIControllerMock(testCase);
                testCase.verifyEqual(methods(bciControllerMock.behavior),...
                    testCase.mockCreator.extractMethodsFromClassName(className));
                testCase.verifyEqual(properties(bciControllerMock.behavior),...
                    testCase.mockCreator.extractPropertiesFromClassName(className));
                success = true;
            catch e
                disp(e);
            end
            testCase.verifyEqual(success, true);
            delete('BCIControllerMock.m');
        end
    end
end



